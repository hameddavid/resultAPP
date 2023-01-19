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
def get_broadsheet_table(stud_reg,unique_courses):
    unique_courses_header = get_formatted_header_query(unique_courses)
    obj = ""
    str_table = ''
    str_table += get_page_header(obj)
    str_table +="<table style='width:100%;border:1;border-collapse:collapse;'>"
    head_tracker = 0
    for main_index, stud in enumerate(stud_reg):
        head_tracker +=1
        tur = str(get_total_unit_reg_in_semester(stud.ug_reg_stud_related.all()) )
        if tur != '0':
             courses_score_dic = get_all_courses_in_dic(stud.ug_reg_stud_related.all())
             if main_index == 0:
                str_table +=get_table_header_row(unique_courses_header)
             str_table += """
        <tr style='border:0;'>
            <td style='border:1px solid black; width:1%;'>"""+ str(main_index+1) +"""</td>
            <td style='border:1px solid black; width:10%;'>"""+ stud.matric_number +"""</td>
            <td style='border:1px solid black;width:30%;'>"""+ stud.surname+"""  """ +stud.firstname+"""</td>
            <td style='border:1px solid black;width:2%;'>"""+tur+"""</td>"""

             for ind,course in enumerate(unique_courses_header):
                str_table +="""<td style='border:1px solid black;width:2%;'>"""+ str(get_score_for_current_course_header(courses_score_dic,course))+"""</td>""" 
             str_table += """</tr> """
             
        if head_tracker == 21:
            str_table += get_page_header(obj)
            head_tracker = 0
 
    str_table += "</table>"
    
    t = Template(str_table)
    c = Context({'test':stud_reg})
    return t.render(c)

def index(request):
    if request.user.is_authenticated:
            return redirect('dashboard')
    stud_reg = Student.objects.prefetch_related(Prefetch('ug_reg_stud_related'
    ,queryset=Registration.objects.filter(session_id='2020/2021', semester='2'))).filter(prog_code='STA',
    current_level='400',status='CURRENT')
    unique_courses = Registration.objects.filter(session_id='2020/2021', semester='1', matric_number_fk__in=stud_reg.values('matric_number')).values('course_code','unit','status').distinct('course_code')
    
    return render(request, 'user/login.html', context={'data':get_broadsheet_table(stud_reg,unique_courses)})


def userlogin(request):
    if request.user.is_authenticated:
            return redirect('dashboard')
    if request.method == "GET":
        return render(request, 'user/login.html')
        
    # try:
    
    if session_semester_config() is not None:
        if not session_semester_config().semester_open_close:
              messages.error(request, f'{session_semester_config().semester_name} {session_semester_config().session} ACADEMIC SESSION is not open')
              return redirect('index')
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
                        return redirect('dashboard')
                    else:
                        messages.error(request, 'Invalid username/password (or inactive account)')
                        return redirect('index')
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
             messages.error(request, "Wrong staff email supplied")
             return redirect('index')
    else:
        messages.error(request, 'No active session/semester, contact Admin')
        return redirect('index')
         
    # except:
        # messages.error(request, 'User does not exist')

    # context = {}
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

def get_score_for_course_header(courses_score_dic,unique_courses_header):
    pass

def get_formatted_header_query(query):
    res_list = []
    track_list = []
    for q in query:
        if q['course_code'] not in track_list:
            res_list.append(q)
            track_list.append(q['course_code'])
    return res_list


def get_score_for_current_course_header(courses_score_dic,course):
     if course['course_code'] in courses_score_dic.keys():
        return courses_score_dic[course['course_code']]
     return ''

def get_table_header_row(unique_courses_header):      
       table_header = """<tr style='border:1px solid black;'>
       <td style='border:1px solid black; width:1%;'> SN</td>
       <td style='border:1px solid black; width:10%;'>Matric Number</td>
       <td style='border:1px solid black;width:22%;'>Names</td>
       <td style='border:1px solid black;width:2%;'>TUR</td>
        """
       for obj in unique_courses_header:
           table_header+= """<td style='border:1px solid black; width:2%;'>"""+ str(obj['course_code'])+ str(obj['unit'])+str(obj['status']) +"""</td>"""
       table_header += """</tr>"""
       return table_header


def get_page_header(obj):
    test = "<h2>Redeemer's University</h2>"
    return  """ <tr style='border:1px solid black;'>
            <td colspan='50' style=' width:1%;'>"""+ test +"""</td>
            </tr>
            """
























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

    
