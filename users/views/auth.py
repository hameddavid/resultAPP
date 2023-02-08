from django.http import HttpResponse, JsonResponse
from django.template import Template, Context
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.db.models import Q,Prefetch
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from base.models import Staff
from users import helpers
from base.baseHelper import session_semester_config, session_semester_config_always
from users.userForm import UserForm
from users.models import User
from course.models import LecturerCourse,Course
import json, os, re,random,string
from django.forms.models import model_to_dict
from undergraduate.models import Course, Curriculum,Student,Department,Programme,RegSummary,Student,Registration
from collections import Counter


# Create your views here.
def unique_user_otp_generator(len):
   try:
     while True:
        otp_rand = "".join(random.choice(string.digits) for x in range(len))
        if(User.objects.filter(otp=otp_rand).exists()):
            continue
        else:
            return otp_rand
   except :
        messages.error("Issue generating unique OTP")
        return redirect('index')

#
def index(request):
    if request.user.is_authenticated:
            return redirect('dashboard')
   
    return render(request, 'user/login.html')


def userlogin(request):
    if request.user.is_authenticated:
            return redirect('dashboard')
    if request.method == "GET":
        return render(request, 'user/login.html')
        
    try:
        if session_semester_config() is not None:
            if not session_semester_config().semester_open_close:
                return JsonResponse({'data':'','status':'Failed','message':f'{session_semester_config().semester_name} {session_semester_config().session} ACADEMIC SESSION is closed'}, safe=False)
            email = request.POST.get('username').lower()
            password = request.POST.get('password')
            user = User.objects.filter(email=email).first()
            if user is not None:
                    if user.semester_session_id == session_semester_config():
                        auth = authenticate(request, email=email, password=password)
                        if auth is not None:
                            login(request,auth)
                            if  f'"{session_semester_config()}.id"' not in user.role.keys():
                                user.role[session_semester_config().id] = []
                                user.save()
                            request.session['settings'] = model_to_dict(session_semester_config())
                            # Lecturer courses for this semester
                            request.session['pendCourses'] = LecturerCourse.objects.filter(Q(lecturer=request.user) & Q(status=0)).count()
                            request.session['appCourses'] = LecturerCourse.objects.filter(Q(lecturer=request.user) & Q(status=10)).count()
                            programmes = Programme.objects.all()
                            # return redirect('dashboard')
                            return JsonResponse({'data':'','status':'success','message':'Login successful!','programmes':programmes}, safe=False)
                        else:
                            return JsonResponse({'data':'','status':'Failed','message':'Invalid username/password (or inactive account)'}, safe=False)

                    else:
                        messages.error(request, f"Kindly activate your account for {session_semester_config().semester_name} {session_semester_config()} academic session")
                        user.otp = unique_user_otp_generator(6)
                        user.save()
                        helpers.semester_activation_email(user)
                        return redirect('semester_activation')
            else:
                staff = Staff.objects.filter(email=email).first()
                if staff is not None:
                    save_user = User.objects.create_user(email = email, password =password,is_active = False, semester_session_id=session_semester_config(),otp=unique_user_otp_generator(6))
                    save_user.save()
                    return redirect('otp')
                else:
                    return JsonResponse({'data':'','status':'Failed','message':'Wrong staff email supplied'}, safe=False)

        else:
            messages.error(request, 'No active session/semester, contact Admin')
            return redirect('index')
            
    except:
        messages.error(request, 'User does not exist')

    return redirect('index')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='index')
def dashboard(request):
    context = {}
    return render(request, 'user/dashboard.html', context)



def logoutUser(request):
    if 'pendCourses' in request.session:
        del request.session['pendCourses']
    if 'appCourses' in request.session:
        del request.session['appCourses']
    logout(request)
    return redirect('index')


def forgotPasswordPage(request):
    context = {}
    return render(request, 'user/forgot.html', context)



def otp(request):
    return render(request, 'user/otp.html')


def semester_activation(request):
    return render(request, 'user/semester_activation.html')

def validateOtp(request):
    get_user_giving_otp = User.objects.filter(otp=request.POST.get('otp')).first()
    if get_user_giving_otp is not None:
        User.objects.filter(otp=request.POST.get('otp')).update(is_active=True, semester_session_id = session_semester_config() )
        messages.error(request, 'Your accout is successfully activated')
        return redirect('index')
    else :
        messages.error(request, 'Invalid six digit OTP supplied')
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'user/otp.html')




def display_class_master_sheet_exam(request):
    # prog_code , level, session_id, semester
    #  CMP 400 , HIS 300, 400, ACC 300
    current_session = session_semester_config().session.split('/')
    stud_reg = [{'matric_number':row.matric_number,
    'surname':row.surname, 'firstname':row.firstname,'sub':row.ug_reg_stud_related.all()} 
        for row in Student.objects.prefetch_related(Prefetch('ug_reg_stud_related'
    ,queryset=Registration.objects.filter(session_id='2021/2022', semester='2'))).filter(prog_code='ACC',
    current_level='300',status='CURRENT').order_by('matric_number')
    if row.ug_reg_stud_related.all().count()>0]
    
    unique_courses = Registration.objects.filter(session_id='2021/2022', semester='2',
    matric_number_fk__in=[mats['matric_number'] for mats in stud_reg]).values('course_code',
    'unit','status','unit_id').distinct('course_code')
    course_desc = Course.objects.filter(course_code__in=[el['course_code'] for el in unique_courses]).order_by('course_code').distinct('course_code')
    
   
    return render(request, 'user/master_sheet.html', context={'data':get_broadsheet_table(stud_reg, unique_courses, course_desc,current_session, request)})



def display_class_master_sheet_summary_exam(request):
    params = {'session_id':'2022/2023','semester':'2', 'prog':'CMP', 'level':'400'}
    
    session_list = [params['session_id']]
    val1 = params['session_id'].split('/')
    current_session = session_semester_config().session.split('/')
    prev_level = int(current_session[1]) - int(val1[1])
    prev_session = f'{str(int(val1[0])-1)}/{str(int(val1[1])-1)}'
    if params['semester'] == '1':
        session_list.append(prev_session)
    stud_reg_sum = [{'matric_number':row.matric_number,
    'surname':row.surname, 'firstname':row.firstname,'summary':row.ug_reg_sum_related.all()} 
    for row in Student.objects.prefetch_related(Prefetch('ug_reg_sum_related'
    ,queryset=RegSummary.objects.filter(session_id__in=session_list))).filter(prog_code= params['prog'],
    current_level=params['level'],status='CURRENT').order_by('matric_number') if [True for val in row.ug_reg_sum_related.all() if val.session_id in session_list ]]

    courses_from_reg = Registration.objects.filter(session_id__lte='2021/2022', status = 'C',
    matric_number_fk__in=[mats['matric_number'] for mats in stud_reg_sum]).values('matric_number_fk',
    'course_code','score','status','grade')
  
    courses_from_curr = Curriculum.objects.filter(programme=params['prog'],status ='C', course_reg_level__lte= str(prev_level)+'00').values('course_code')
    
    return render(request, 'user/master_sheet_summary.html', context={'data':get_summary_table(stud_reg_sum,courses_from_reg,courses_from_curr,current_session,request)})




def prepare_get_values_for_summary_sheet(summary_instance,courses_from_reg, courses_from_curr,request):
    # params = {'session_id':'2021/2022','semester':'1', 'prog':'ECO', 'level':'300'}
    # params = {'session_id':'2022/2023','semester':'1', 'prog':'CMP', 'level':'400'}
    params = {'session_id':'2022/2023','semester':'2', 'prog':'CMP', 'level':'400'}
    t_str = ''
    prev = {}
    curr = list(filter(lambda row:row.session_id == params['session_id'] and row.semester == params['semester'], summary_instance))
    if params['semester'] == '2':
        prev = list(filter(lambda row:row.session_id == params['session_id'] and row.semester == '1', summary_instance))
    elif params['semester'] == '1':
        prev_session_list = params['session_id'].split('/')
        prev_session = str(int(prev_session_list[0])-1)+'/'+str(int(prev_session_list[1])-1)
        prev = list(filter(lambda row:row.session_id == prev_session and row.semester == '2', summary_instance))
  
    if len(prev)>0 and len(curr)>0:
        # There is previous and current summary
        t_str +="""
        <td>"""+control_null_value_2(prev[0].ctnur) +"""</td>
        <td>"""+control_null_value_2(prev[0].ctnup) +"""</td>
        <td>"""+control_null_value_2(prev[0].ctcp) +"""</td>
        <td>"""+control_null_value_1(prev[0].cgpa) +"""</td>
        <td>"""+control_null_value_2(curr[0].tnur) +"""</td>
        <td>"""+control_null_value_2(curr[0].tnup) +"""</td>
        <td>"""+control_null_value_2(curr[0].wcrp) +"""</td>
        <td>"""+control_null_value_1(curr[0].gpa)+"""</td>
        <td>"""+str(get_stud_oustanding(curr[0], courses_from_reg, courses_from_curr, request)[0]) +"""</td>
        <td>"""+control_null_value_2(curr[0].ctnur) +"""</td>
        <td>"""+control_null_value_2(curr[0].ctnup) +"""</td>
        <td>"""+control_null_value_2(curr[0].ctcp) +"""</td>
        <td>"""+control_null_value_1(curr[0].cgpa) +"""</td>
        <td>"""+str(get_stud_oustanding(curr[0], courses_from_reg, courses_from_curr, request)[1]) +"""</td>
        <td>"""+str(curr[0].acad_status) +"""</td>"""
    elif len(prev) == 0 and len(curr)>0:          
        # There is no previous summary
        t_str +="""<td>-</td><td>-</td><td>-</td><td>-</td>
            <td>""" + control_null_value_2(curr[0].tnur) + """</td>
        <td>"""+control_null_value_2(curr[0].tnup) +"""</td>
        <td>"""+control_null_value_2(curr[0].wcrp) +"""</td>
        <td>"""+control_null_value_1(curr[0].gpa) +"""</td>
        <td>"""+str(get_stud_oustanding(curr[0], courses_from_reg, courses_from_curr, request)[0]) +"""</td>
        <td>"""+control_null_value_2(curr[0].ctnur) +"""</td>
        <td>"""+control_null_value_2(curr[0].ctnup) +"""</td>
        <td>"""+control_null_value_2(curr[0].ctcp) +"""</td>
        <td>"""+control_null_value_1(curr[0].cgpa) +"""</td>
        <td>"""+str(get_stud_oustanding(curr[0], courses_from_reg, courses_from_curr, request)[1]) +"""</td>
        <td>"""+str(curr[0].acad_status) +"""</td>"""
    elif len(prev) > 0 and len(curr)==0:  
        # There is previous summary only
        t_str +="""
        <td>"""+control_null_value_2(prev[0].ctnur) +"""</td>
        <td>"""+control_null_value_2(prev[0].ctnup) +"""</td>
        <td>"""+control_null_value_2(prev[0].ctcp) +"""</td>
        <td>"""+control_null_value_1(prev[0].cgpa) +"""</td>"""

    return t_str


def control_null_value_1(val):
    if val is None:
        return ' '
    else:
        return str(round(val,2))

def control_null_value_2(val):
    if val is None:
        return ' '
    else:
        return str(round(val))


def get_stud_oustanding(curr,courses_from_reg,courses_from_curr, request):
    list_reg_courses = [row['course_code'] for row in courses_from_reg if row['matric_number_fk'] == f'{curr.matric_number_fk}']
    list_reg_failed_courses = [row['course_code'] for row in courses_from_reg if row['matric_number_fk'] == f'{curr.matric_number_fk}' and row['grade']=='F']
    list_curr_courses = [row['course_code'] for row in courses_from_curr]
    courses_in_curr_not_reg = list((Counter(list_curr_courses) - Counter(list_reg_courses)).elements())
    if len(list_reg_courses) > 0:
          courses_in_curr_not_reg = [f'*{course}' for course in courses_in_curr_not_reg]
    courses = ''
    combined = list_reg_failed_courses + courses_in_curr_not_reg
    for index, course in enumerate(combined, start=1):
        courses += course
        if index != len(combined):
            courses += ' , '
    return [len(list_reg_failed_courses + courses_in_curr_not_reg),courses]


def get_total_unit_reg_in_semester(query):
    unit = 0
    for rec in query:
        unit += rec.unit
    return unit

def get_all_courses_in_dic(courses):
    list_courses = {}
    for course in courses:
        list_courses[course.course_code] = course.score
    return list_courses


def get_formatted_header_query(query):
    res_list = []
    track_list = []
    for q in query:
        if q['course_code'] not in track_list:
            res_list.append(q)
            track_list.append(q['course_code'])
    return res_list

def get_unique_courses_desc(query):
    res_list = []
    track_list = []
    for q in query:
        if q.course_code not in track_list:
            res_list.append({'course_code':q.course_code,'course_title':q.course_title})
            track_list.append(q.course_code)
    res = """<table class="result_table"> 
            <tr><th style="text-align: left" >SN</th><th style="text-align: left">Course Code</th><th style="text-align: left">Course Title</th></tr>
       """
    if len(res_list) > 0:
        for index, row in enumerate(res_list, start=1):
            res += """<tr><td>"""+ str(index)+"""</td><td>"""+row['course_code']+"""</td><td>"""+row['course_title']+"""</td></tr>"""
    res +="</table>"
    return res

def get_score_for_current_course_header(courses_score_dic,course):
     if course['course_code'] in courses_score_dic.keys():
        return courses_score_dic[course['course_code']]
     return ''

def get_table_header_row(unique_courses_header):      
       table_header = """<tr >
       <th > SN</th>
       <th >Matric Number</th>
       <th >Names</th>
       <th >TUR</th>
        """
       for obj in unique_courses_header:
           table_header+= """<th valign="top" >
           """+  str(obj['course_code'])+""" <h6 > """+ str(obj['unit'])+"""</h6><h6 ">
           """ +str(obj['status']) +"""</h6></th>"""
       table_header += """</tr>"""
       return table_header


def get_page_header(request, current_session):
    val1 = '2019/2020'.split('/')
    val2 = current_session

    details = {'faculty':'SMS', 'department':'Economics','program':'Economics','level':'200','semester':'1','session':'2020/2021'}

    return  """   <div class="page"> {% load static %}
            <div class="header">
                <img src="{% static '/images/run_logo_big.png'%}" class="logo"/>
		<h1>REDEEMER\'S UNIVERSITY</h1>
		<h5>MASTER SHEET FOR PRESENTATION OF EXAMINATION RESULTS</h5>
         <table>
		    <tr>
			<td style="text-align: left">FACULTY OF: <strong>""" + details["faculty"] + """</strong></td>
			<td style="text-align: left">Department OF: <strong>""" + details["department"] + """</strong></td>
		    </tr>
		    <tr>
			<td style="text-align: left">PROGRAMME: <strong>""" + details["program"] + """</strong></td>
			<td style="text-align: left">LEVEL: <strong>""" + details["level"] + """</strong></td>
		    </tr>
		    <tr>
			<td style="text-align: left">SESSION: <strong>""" + details["session"] + """</strong></td>
			<td style="text-align: left">SEMESTER: <strong>""" + details["semester"] + """</strong></td>
		    </tr>
		</table>
	    </div>
            <div class="header2">
       
	    </div>"""
            

def get_static_table_header_for_summary_sheet():
    return """<table class="result_table" >
    <tr><th>SN </th> <th> Matric Number</th> <th>Names </th> <th>Prev CTNUR </th>
    <th>Prev CTNUP </th> <th>Prev CTCP </th> <th>Prev CGPA </th>
    <th>Curr TNUR </th> <th>Curr TNUP </th> <th> Curr TCP </th> <th>Curr GPA </th>
    <th>Outstd</th> <th>CTNUR </th> <th> CTNUP </th> <th> CTCP </th> <th> CGPA </th>
    <th> Outstanding Course </th> <th>Status</th>
    </tr>
    """

def get_summary_sheet_abbr_details():
    return """<table class="result_table" >
    <tr><th>SN </th> <th> Matric Number</th> <th>Names </th> <th>Prev CTNUR </th>
    <th>Prev CTNUP </th> <th>Prev CTCP </th> <th>Prev CGPA </th>
    <th>Curr TNUR </th> <th>Curr TNUP </th> <th> Curr TCP </th> <th>Curr GPA </th>
    <th>Outstd</th> <th>CTNUR </th> <th> CTNUP </th> <th> CTCP </th> <th> CGPA </th>
    <th> Outstanding Course </th> <th>Status</th>
    </tr></table>
    """


def get_summary_table(stud_reg_sum,courses_from_reg,courses_from_curr,current_session,request):
    table_data = ''
    table_data += get_page_header(request,current_session)
    head_tracker = 0
    sn = 0
    for main_index, stud in enumerate(stud_reg_sum, start=1):
        head_tracker +=1
        if main_index == 1:
                table_data +=  get_static_table_header_for_summary_sheet()
        firstName = stud['firstname'].split(' ') 
        val_prepare_get_values_for_summary_sheet = prepare_get_values_for_summary_sheet(stud['summary'],courses_from_reg,courses_from_curr,request)
        if val_prepare_get_values_for_summary_sheet == '':
            continue
        sn +=1
        table_data += """<tr><td>"""+ str(sn) + """</td>
         <td>"""+ stud['matric_number'] + """</td>
         <td> """+ stud['surname'] + """   """+firstName[0] +"""</td>
         """+val_prepare_get_values_for_summary_sheet+"""
         </tr>"""
        if head_tracker == 20:
                table_data += """</table></div></br></br>""" 
                table_data +=get_page_header(request,current_session)+get_static_table_header_for_summary_sheet()
                head_tracker = 0
        if main_index == len(stud_reg_sum):
            if head_tracker <= 10:
                table_data += """</table></br></br>"""+get_summary_sheet_abbr_details()+"""</div>"""
            elif head_tracker > 10:
                 table_data += """</table></div></br></br>""" 
                 table_data +=get_page_header(request,current_session)+get_summary_sheet_abbr_details()+"""</table></div>"""
        # if main_index == 4:
        #     break
    t = Template(table_data)
    c = Context({'test':stud_reg_sum})
    return t.render(c)

    
def get_broadsheet_table(stud_reg, unique_courses, course_desc,current_session, request):
    unique_courses_header = get_formatted_header_query(unique_courses)
    str_table = ''
    str_table += get_page_header(request,current_session)
    head_tracker = 0
    for main_index, stud in enumerate(stud_reg, start=1): 
        tur = str(get_total_unit_reg_in_semester(stud['sub']) )
        if main_index == 1:
                str_table += """<table class="result_table" >"""
                str_table +=get_table_header_row(unique_courses_header)
        head_tracker +=1
        firstName = stud['firstname'].split(' ')
        courses_score_dic = get_all_courses_in_dic(stud['sub'])
        str_table += """ <tr >
    <td style="text-align: left">"""+ str(main_index) +"""</td>
    <td style="text-align: left">"""+ stud['matric_number'] +"""</td>
    <td style="text-align: left">"""+ stud['surname']+"""  """ +firstName[0]+"""</td>
    <td style="text-align: center">"""+tur+"""</td>"""
        for ind,course in enumerate(unique_courses_header):
            str_table +="""<td style="text-align: center;">"""+ str(get_score_for_current_course_header(courses_score_dic,course))+"""</td>""" 
        str_table += """</tr> """  
        
        if head_tracker == 20:
                str_table += """</table></div></br></br>"""
                if  len(stud_reg) != main_index :
                    str_table +=get_page_header(request,current_session)+"""<table class="result_table">"""+get_table_header_row(unique_courses_header)
                head_tracker = 0
        # if (len(stud_reg)-main_index) < 20 :
        #     if head_tracker <= 10:
        #         str_table += """</table></br></br>"""+get_unique_courses_desc(course_desc)+"""</div>"""
        #     elif head_tracker > 10:
        #          str_table += """</table></div></br></br>""" 
        #          str_table +=get_page_header(request)+get_unique_courses_desc(course_desc)+"""</table></div>"""
        if len(stud_reg)  == main_index :
                str_table += """</table></div></br></br>""" 
                str_table +=get_page_header(request,current_session)+get_unique_courses_desc(course_desc)+"""</table></div>"""
    str_table += "</table>" 
    t = Template(str_table)
    c = Context({'test':stud_reg})
    return t.render(c)















# def userlogin(request):
#     if request.user.is_authenticated:
#             return redirect('dashboard')
#     if request.method == "GET":
#         return render(request, 'user/login.html')
        
#     # try:
    
#     if session_semester_config() is not None:
#         if not session_semester_config().semester_open_close:
#             #   messages.error(request, f'{session_semester_config().semester_name} {session_semester_config().session} ACADEMIC SESSION is closed')
#             #   return redirect('index')
#             return JsonResponse({'status':'Failed','message':f'{session_semester_config().semester_name} {session_semester_config().session} ACADEMIC SESSION is closed'}, safe=False)
#         email = request.POST.get('username').lower()
#         password = request.POST.get('password')
#         user = User.objects.filter(email=email).first()
#         if user is not None:
#                 if user.semester_session_id == session_semester_config():
#                     auth = authenticate(request, email=email, password=password)
#                     if auth is not None:
#                         login(request,auth)
#                         if  f'"{session_semester_config()}.id"' not in user.role.keys():
#                              user.role[session_semester_config().id] = []
#                              user.save()
#                         request.session['settings'] = model_to_dict(session_semester_config())
#                         # Lecturer courses for this semester
#                         request.session['pendCourses'] = LecturerCourse.objects.filter(Q(lecturer=request.user) & Q(status=0)).count()
#                         request.session['appCourses'] = LecturerCourse.objects.filter(Q(lecturer=request.user) & Q(status=10)).count()
#                         return redirect('dashboard')
#                     else:
#                         messages.error(request, 'Invalid username/password (or inactive account)')
#                         return redirect('index')
#                 else:
#                     messages.error(request, f"Kindly activate your account for {session_semester_config().semester_name} {session_semester_config()} academic session")
#                     user.otp = unique_user_otp_generator(6)
#                     user.save()
#                     helpers.semester_activation_email(user)
#                     return redirect('semester_activation')
#         else:
#            staff = Staff.objects.filter(email=email).first()
#            if staff is not None:
#               save_user = User.objects.create_user(email = email, password =password,is_active = False, semester_session_id=session_semester_config(),otp=unique_user_otp_generator(6))
#               save_user.save()
#               return redirect('otp')
#            else:
#              messages.error(request, "Wrong staff email supplied")
#              return redirect('index')
#     else:
#         messages.error(request, 'No active session/semester, contact Admin')
#         return redirect('index')
         
#     # except:
#         # messages.error(request, 'User does not exist')

#     # context = {}
#     return redirect('index')






# def reset_password(request):
#     user = User.objects.filter(email=request.POST.get('email'))

#     user.set_password(password)
#     user.save()
#     return "Password has been changed successfully"
   
    # try:
    #     user = User.objects.get(username=u)
    # except:
    #     return "User could not be found"
    # user.set_password(password)
    # user.save()
    # return "Password has been changed successfully"

    
    
#  SELECT DISTINCT `matric_number` AS s_matric_number , `programme` AS s_program  ,
#          `course_status` AS s_course_status , `course_code` AS s_course_code ,
#          `course_id` AS s_course_id ,`t_courses`.`_unit` AS s_course_unit ,
#          t_registrations.registration_level, t_registrations.last_update_date as dt_date
#          FROM t_registrations INNER JOIN t_course_registered ON 
#           `registration_id` =`registration_id_FK` 
#            INNER JOIN `t_students`  ON `t_registrations`.`matric_number_FK` =
#             `matric_number` INNER JOIN `t_programmes` ON`programme_id` =`programme_id_FK` 
#              INNER JOIN `t_courses` ON`course_id` =`course_id_FK` 
#               WHERE `semester_id_FK` = 22  
#                 AND `t_registrations`.`registration_level` =`t_students`.`current_level` 
#                  and length(trim(matric_number)) > 5
#               ORDER BY  t_registrations.last_update_date,matric_number ASC; 