from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import Template,Context
from django.db.models import Q,Prefetch
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from collections import Counter
from django.contrib.auth.decorators import login_required
from undergraduate.models import Course,Curriculum,LecturerCourse
from users.models import User
from base.models import Setting
from base.baseHelper import session_semester_config, session_semester_config_always
from undergraduate.models import Course, Curriculum,Student,Department,Programme,Faculty,RegSummary,Registration




@login_required(login_url='index')
def get_print_result_view(request):
    
    if request.user.user_roles_hod:
        print("HOD @@@@@@@@@@@@@@@@@@@@@@@@@")
        pass
    sessions = Setting.objects.all().distinct('session').order_by('-session')

    return render(request, 'result/printResults.html',{'sessions':sessions})




# def display_class_master_sheet_exam(request):
#     # prog_code , level, session_id, semester
#     #  CMP 400 , HIS 300, 400, ACC 300
#     current_session = session_semester_config().session.split('/')
#     stud_reg = [{'matric_number':row.matric_number,
#     'surname':row.surname, 'firstname':row.firstname,'sub':row.ug_reg_stud_related.all()} 
#         for row in Student.objects.prefetch_related(Prefetch('ug_reg_stud_related'
#     ,queryset=Registration.objects.filter(session_id='2021/2022', semester='2'))).filter(prog_code='ACC',
#     current_level='300',status='CURRENT').order_by('matric_number')
#     if row.ug_reg_stud_related.all().count()>0]
    
#     unique_courses = Registration.objects.filter(session_id='2021/2022', semester='2',
#     matric_number_fk__in=[mats['matric_number'] for mats in stud_reg]).values('course_code',
#     'unit','status','unit_id').distinct('course_code')
#     course_desc = Course.objects.filter(course_code__in=[el['course_code'] for el in unique_courses]).order_by('course_code').distinct('course_code')
    
   
#     return render(request, 'user/master_sheet.html', context={'data':get_broadsheet_table(stud_reg, unique_courses, course_desc,current_session, request)})



# def display_class_master_sheet_summary_exam(request):
#     # params = {'session_id':'2022/2023','semester':'2', 'prog':'CMP', 'level':'300'}
#     params = {'session_id':'2021/2022','semester':'1', 'prog':'ECO', 'level':'300'}
    
#     session_list = [request.POST['session']]
#     val1 = request.POST['session'].split('/')
#     current_session = session_semester_config().session.split('/')
#     prev_level = int(current_session[1]) - int(val1[1])
#     prev_session = f'{str(int(val1[0])-1)}/{str(int(val1[1])-1)}'
#     if params['semester'] == '1':
#         session_list.append(prev_session)
#     stud_reg_sum = [{'matric_number':row.matric_number,
#     'surname':row.surname, 'firstname':row.firstname,'summary':row.ug_reg_sum_related.all()} 
#     for row in Student.objects.prefetch_related(Prefetch('ug_reg_sum_related'
#     ,queryset=RegSummary.objects.filter(session_id__in=session_list))).filter(prog_code= params['prog'],
#     current_level=params['level'],status='CURRENT').order_by('matric_number') 
#     if [True for val in row.ug_reg_sum_related.all() if val.session_id in session_list ]]

#     courses_from_reg = Registration.objects.filter(session_id__lte=request.POST['session'], status = 'C',
#     matric_number_fk__in=[mats['matric_number'] for mats in stud_reg_sum]).values('matric_number_fk',
#     'course_code','score','status','grade')
  
#     courses_from_curr = Curriculum.objects.filter(programme=params['prog'],status ='C', course_reg_level__lte= str(prev_level)+'00').values('course_code')
    
#     return render(request, 'user/master_sheet_summary.html', context={'data':get_summary_table(stud_reg_sum,courses_from_reg,courses_from_curr,current_session,request)})


def validate_request_parama(request):
     # <QueryDict: {'csrfmiddlewaretoken': ['u29Nz5txhyu8gvDdmjTU2Buwifp7cWpHHH9cZUTgGdqpal2Qchvx4anzYBbcDQaJ'], 
    # 'to_print': ['summary'], 'group': ['current'], 
    # 'level': ['200'], 'session': ['2008/2009'], 'semester': ['1']}>
    return True


def get_broadsheet_or_summary_for_print(request):

    if validate_request_parama(request):
        get_programme = request.user.programme
        session_list = [request.POST['session']]
        val1 = request.POST['session'].split('/')
        current_session = session_semester_config().session.split('/')
        prev_level = str(int(current_session[1]) - int(val1[1]))+'00'
        prev_session = f'{str(int(val1[0])-1)}/{str(int(val1[1])-1)}'
        
        if request.POST['to_print'].upper() == 'SUMMARY':
            cur_result = [{'matric_number':row.matric_number,
            'surname':row.surname, 'firstname':row.firstname,'sub':row.ug_reg_stud_related.all()} 
                for row in Student.objects.prefetch_related(Prefetch('ug_reg_stud_related'
            ,queryset=Registration.objects.filter(session_id=request.POST['session'], deleted='N'))
            ).filter(prog_code=get_programme,
            current_level=request.POST['level'],status=request.POST['group']).order_by('matric_number')
            if row.ug_reg_stud_related.all().count()>0]

            cur_prev_result = [{'matric_number':row.matric_number,
            'surname':row.surname, 'firstname':row.firstname,'sub':row.ug_reg_stud_related.all()} 
                for row in Student.objects.prefetch_related(Prefetch('ug_reg_stud_related'
            ,queryset=Registration.objects.filter(session_id__lte=request.POST['session'], deleted='N'))
            ).filter(prog_code=get_programme,
            current_level=request.POST['level'],status=request.POST['group'],
            matric_number__in=[mats['matric_number'] for mats in cur_result]).order_by('matric_number')
            if row.ug_reg_stud_related.all().count()>0]
    
            courses_from_reg = Registration.objects.filter(session_id__lte=request.POST['session'], status = 'C',
            matric_number_fk__in=[mats['matric_number'] for mats in cur_result]).values('matric_number_fk',
            'course_code','score','status','grade')
        
            courses_from_curr = Curriculum.objects.filter(programme=get_programme,status ='C', course_reg_level__lte= prev_level).values('course_code')
            
            return render(request, 'user/master_sheet_summary.html', context={'data':get_summary_table_2(cur_prev_result,courses_from_reg,courses_from_curr,prev_level,request)})
        
        elif request.POST['to_print'].upper() == 'BROADSHEET':
               stud_reg = [{'matric_number':row.matric_number,
                'surname':row.surname, 'firstname':row.firstname,'sub':row.ug_reg_stud_related.all()} 
                    for row in Student.objects.prefetch_related(Prefetch('ug_reg_stud_related'
                ,queryset=Registration.objects.filter(session_id=request.POST['session'], semester=request.POST['semester'])
                )).filter(prog_code=get_programme,current_level=request.POST['level'],status=request.POST['group']).order_by('matric_number')
                if row.ug_reg_stud_related.all().count()>0]
                
               unique_courses = Registration.objects.filter(session_id=request.POST['session'], semester=request.POST['semester'],
                matric_number_fk__in=[mats['matric_number'] for mats in stud_reg]).values('course_code',
                'unit','status','unit_id').distinct('course_code')
               course_desc = Course.objects.filter(course_code__in=[el['course_code'] for el in unique_courses]).order_by('course_code').distinct('course_code')
                
               return render(request, 'user/master_sheet.html', context={'data':get_broadsheet_table(stud_reg, unique_courses, course_desc,prev_level, request)})

        else:
            messages.error(request, 'Unknown "type to print" selected')
            return redirect('get_print_result_view')
    else:
        messages.error(request, 'Error in paramter supplied')
        return redirect('get_print_result_view')



# def display_class_master_sheet_summary_exam_direct_from_reg_table(request):
#     # params = {'session_id':'2022/2023','semester':'2', 'prog':'CMP', 'level':'300'}
#     params = {'session_id':'2021/2022','semester':'1', 'prog':'CMP', 'level':'400'}
#     session_list = [request.POST['session']]
#     val1 = request.POST['session'].split('/')
#     current_session = session_semester_config().session.split('/')
#     prev_level = int(current_session[1]) - int(val1[1])
#     prev_session = f'{str(int(val1[0])-1)}/{str(int(val1[1])-1)}'
#     current_session = session_semester_config().session.split('/')

#     cur_result = [{'matric_number':row.matric_number,
#     'surname':row.surname, 'firstname':row.firstname,'sub':row.ug_reg_stud_related.all()} 
#         for row in Student.objects.prefetch_related(Prefetch('ug_reg_stud_related'
#     ,queryset=Registration.objects.filter(session_id=request.POST['session'], deleted='N'))).filter(prog_code=params['prog'],
#     current_level=params['level'],status='CURRENT').order_by('matric_number')
#     if row.ug_reg_stud_related.all().count()>0]

#     cur_prev_result = [{'matric_number':row.matric_number,
#     'surname':row.surname, 'firstname':row.firstname,'sub':row.ug_reg_stud_related.all()} 
#         for row in Student.objects.prefetch_related(Prefetch('ug_reg_stud_related'
#     ,queryset=Registration.objects.filter(session_id__lte=request.POST['session'], deleted='N'))).filter(prog_code=params['prog'],
#     current_level=params['level'],status='CURRENT',
#     matric_number__in=[mats['matric_number'] for mats in cur_result]).order_by('matric_number')
#     if row.ug_reg_stud_related.all().count()>0]
    
#     # return render(request, 'user/master_sheet_summary_2.html', context={'data':cur_result})

#     courses_from_reg = Registration.objects.filter(session_id__lte='2021/2022', status = 'C',
#     matric_number_fk__in=[mats['matric_number'] for mats in cur_result]).values('matric_number_fk',
#     'course_code','score','status','grade')
  
#     courses_from_curr = Curriculum.objects.filter(programme=params['prog'],status ='C', course_reg_level__lte= str(prev_level)+'00').values('course_code')
    
   
#     return render(request, 'user/master_sheet_summary.html', context={'data':get_summary_table_2(cur_prev_result,cur_result,courses_from_reg,courses_from_curr,current_session,request,params)})



def prepare_get_values_for_summary_sheet_2(subjects,courses_from_reg, courses_from_curr,request,stud):
    t_str = ''
    t_str +="""<td>"""+ str(get_prev_ctnur(subjects, session=request.POST['session'])) + """</td> """
    t_str +="""<td>"""+ str(get_prev_ctnup(subjects, session=request.POST['session'])) + """</td> """
    t_str +="""<td>"""+ str(get_prev_ctcp(subjects, session=request.POST['session'])) + """</td> """
    t_str +="""<td>"""+ str(get_prev_cgpa(get_prev_ctnur(subjects, session=request.POST['session']), get_prev_ctcp(subjects, session=request.POST['session']))) + """</td> """
    
    t_str +="""<td>"""+ str(get_cur_ctnur(subjects, session=request.POST['session'],semester=request.POST['semester'])) + """</td> """
    t_str +="""<td>"""+ str(get_cur_ctnup(subjects, session=request.POST['session'],semester=request.POST['semester'])) + """</td> """
    t_str +="""<td>"""+ str(get_cur_ctcp(subjects, session=request.POST['session'],semester=request.POST['semester'])) + """</td> """
    t_str +="""<td>"""+ str(get_cur_gpa( get_cur_ctnur(subjects, session=request.POST['session'],semester=request.POST['semester']), get_cur_ctcp(subjects, session=request.POST['session'],semester=request.POST['semester']) ) ) + """</td> """
    t_str +="""<td>"""+str(get_stud_oustanding_2(stud, courses_from_reg, courses_from_curr, request)[0]) +"""</td>"""
    
    t_str +="""<td>"""+ str(format_for_str_issue(get_prev_ctnur(subjects, session=request.POST['session']), get_cur_ctnur(subjects, session=request.POST['session'],semester=request.POST['semester']))) + """</td> """
    t_str +="""<td>"""+ str( format_for_str_issue(get_prev_ctnup(subjects, session=request.POST['session']) , get_cur_ctnup(subjects, session=request.POST['session'],semester=request.POST['semester']))) + """</td> """
    t_str +="""<td>"""+ str( format_for_str_issue(get_prev_ctcp(subjects, session=request.POST['session']) , get_cur_ctcp(subjects, session=request.POST['session'],semester=request.POST['semester']))) + """</td> """
    t_str +="""<td>"""+ str(get_cgpa(
        get_prev_ctnur(subjects, session=request.POST['session']),
        get_prev_ctcp(subjects, session=request.POST['session']),
        get_cur_ctnur(subjects, session=request.POST['session'],semester=request.POST['semester']),
        get_cur_ctcp(subjects, session=request.POST['session'],semester=request.POST['semester'])
    )) + """</td> """
    t_str +="""<td>"""+str(get_stud_oustanding_2(stud, courses_from_reg, courses_from_curr, request)[1]) +"""</td>"""
    t_str +="""<td>"""+str(get_acad_status(get_cgpa(
        get_prev_ctnur(subjects, session=request.POST['session']),
        get_prev_ctcp(subjects, session=request.POST['session']),
        get_cur_ctnur(subjects, session=request.POST['session'],semester=request.POST['semester']),
        get_cur_ctcp(subjects, session=request.POST['session'],semester=request.POST['semester'])
    )))+"""</td>"""
    
    return t_str





def get_prev_cgpa(get_prev_ctnur,get_prev_ctcp):
    if get_prev_ctnur != 0 and not isinstance(get_prev_ctnur, str) and not isinstance(get_prev_ctcp, str):
        return round(int(get_prev_ctcp)/int(get_prev_ctnur),2)
    return '-'

def get_cur_gpa(get_cur_ctnur,get_cur_ctcp):
    if get_cur_ctnur != 0 and not isinstance(get_cur_ctnur, str) and not isinstance(get_cur_ctcp, str):
        return round(int(get_cur_ctcp)/int(get_cur_ctnur),2)
    return '-'

def get_cgpa(get_prev_ctnur,get_prev_ctcp,get_cur_ctnur,get_cur_ctcp):
    divisor = 0
    if not isinstance(get_prev_ctnur, str) and not isinstance(get_cur_ctnur, str) and not isinstance(get_prev_ctcp, str)and not isinstance(get_cur_ctcp, str):
        divisor = get_prev_ctnur + get_cur_ctnur
        if divisor != 0 :
            return round((int(get_prev_ctcp)+ int(get_cur_ctcp))/int(divisor),2)
    elif isinstance(get_prev_ctnur, str)  and isinstance(get_prev_ctcp, str) and not isinstance(get_cur_ctnur, str) and not isinstance(get_cur_ctcp, str):
        divisor = get_cur_ctnur
        if divisor !=0:
            return round(int(get_cur_ctcp)/int(divisor),2)
    elif not isinstance(get_prev_ctnur, str)  and not isinstance(get_prev_ctcp, str) and  isinstance(get_cur_ctnur, str) and  isinstance(get_cur_ctcp, str):
        divisor = get_prev_ctnur
        if divisor !=0:
            return round(int(get_prev_ctcp)/int(divisor),2)
    return '-'


def format_for_str_issue(para1, para2):
    var1 = 0 if isinstance(para1, str) else para1
    var2 = 0 if isinstance(para2, str) else para2
    return int(var1) + int(var2)

def get_prev_ctcp(courses,session):
    prev_ctcp = 0
    for row in courses:
        if  row.session_id < session:
            prev_ctcp += int(row.unit) * int(get_point_from_score(row.score))
    if prev_ctcp > 0:
        return prev_ctcp
    else: 
        return '-'

def get_cur_ctcp(courses,session,semester):
    prev_ctcp = 0
    for row in courses:
        if  row.session_id == session and row.semester == semester:
            prev_ctcp += int(row.unit) * int(get_point_from_score(row.score))
    if prev_ctcp > 0:
        return prev_ctcp
    else: 
        return '-'

def get_point_from_score(score):
  if score >= 70 :
    return 5
  elif  score >= 60 and score < 70 :
    return 4  
  elif score >= 50 and score < 60 :
    return 3
  elif  score >= 45 and score < 50 :
    return 2
  elif  score >= 40 and score < 45 :
    return 1
  elif  score < 40 :
    return 0



def get_prev_ctnup(courses,session):
    prev_ctnup = 0
    for row in courses:
        if row.score >= 40 and row.session_id < session:
            prev_ctnup += int(row.unit)
    if prev_ctnup > 0:
        return prev_ctnup
    else: 
        return '-'

def get_cur_ctnup(courses,session, semester):
    prev_ctnup = 0
    for row in courses:
        if row.score >= 40 and row.session_id == session and row.semester == semester:
            prev_ctnup += int(row.unit)
    if prev_ctnup > 0:
        return prev_ctnup
    else: 
        return '-'

def get_prev_ctnur(courses, session):
    prev_ctnur = 0
    for row in courses:
        if row.session_id < session:
            prev_ctnur += int(row.unit)
    if prev_ctnur > 0:
        return prev_ctnur
    else: 
        return '-'

def get_cur_ctnur(courses, session, semester):
    prev_ctnur = 0
    for row in courses:
        if row.session_id == session and row.semester == semester:
            prev_ctnur += int(row.unit)
    if prev_ctnur > 0:
        return prev_ctnur
    else: 
        return '-'

def get_acad_status(cgpa):
    if isinstance(cgpa, str):
        return 'None'
    if cgpa >= 4.50:
        return 'Good Standing (Excellent)'
    elif  cgpa >= 3.50 and cgpa <= 4.49:
        return 'Good Standing (Very Good)'
    elif  cgpa >= 2.50 and cgpa <= 3.49:
        return 'Good Standing (Good)'
    elif  cgpa >= 1.50 and cgpa <= 2.49:
        return 'Good Standing (Average)'
    elif  cgpa >= 1.00 and cgpa <= 1.49:
        return 'Probation (Fair)'
    elif  cgpa < 1.00 :
        return 'Warning (Very Poor)'


def prepare_get_values_for_summary_sheet(summary_instance,courses_from_reg, courses_from_curr,request):
    params = {'session_id':'2021/2022','semester':'1', 'prog':'ECO', 'level':'300'}
    # params = {'session_id':'2022/2023','semester':'1', 'prog':'CMP', 'level':'400'}
    # params = {'session_id':'2022/2023','semester':'2', 'prog':'CMP', 'level':'300'}
    t_str = ''
    prev = {}
    curr = list(filter(lambda row:row.session_id == request.POST['session'] and row.semester == params['semester'], summary_instance))
    if params['semester'] == '2':
        prev = list(filter(lambda row:row.session_id == request.POST['session'] and row.semester == '1', summary_instance))
    elif params['semester'] == '1':
        prev_session_list = request.POST['session'].split('/')
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


def get_stud_oustanding_2(stud,courses_from_reg,courses_from_curr, request):
    list_reg_courses = [row['course_code'] for row in courses_from_reg if row['matric_number_fk'] == f"{stud['matric_number']}"]
    list_reg_failed_courses = [row['course_code'] for row in courses_from_reg if row['matric_number_fk'] == f"{stud['matric_number']}" and row['grade']=='F']
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


def get_page_header(request, prev_level):
    
    faculty = Faculty.objects.filter(id = request.user.faculty.id).first().faculty if Faculty.objects.filter(id = request.user.faculty.id).first().faculty else " "
    dept = Department.objects.filter(id = request.user.department.id).first().department if Department.objects.filter(id = request.user.department.id).first().department else " "
    prog = Programme.objects.filter(programme_id = request.user.programme.programme_id).first().programme if Programme.objects.filter(programme_id = request.user.programme.programme_id).first().programme else " "
  
    return  """   <div class="page"> {% load static %}
            <div class="header">
                <img src="{% static '/images/run_logo_big.png'%}" class="logo"/>
		<h1>REDEEMER\'S UNIVERSITY</h1>
		<h5>MASTER SHEET FOR PRESENTATION OF EXAMINATION RESULTS</h5>
         <table>
		    <tr>
			<td style="text-align: left">FACULTY OF: <strong>""" + str(faculty) + """</strong></td>
			<td style="text-align: left">Department OF: <strong>""" + str(dept) + """</strong></td>
		    </tr>
		    <tr>
			<td style="text-align: left">PROGRAMME: <strong>""" + str(prog) + """</strong></td>
			<td style="text-align: left">LEVEL: <strong>""" + str(prev_level) + """</strong></td>
		    </tr>
		    <tr>
			<td style="text-align: left">SESSION: <strong>""" + str(request.POST["session"]) + """</strong></td>
			<td style="text-align: left">SEMESTER: <strong>""" + str(request.POST["semester"]) + """</strong></td>
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


def get_summary_table(stud_reg_sum,courses_from_reg,courses_from_curr,prev_level,request):
    table_data = ''
    table_data += get_page_header(request,prev_level)
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
                table_data +=get_page_header(request,prev_level)+get_static_table_header_for_summary_sheet()
                head_tracker = 0
        if main_index == len(stud_reg_sum):
            if head_tracker <= 10:
                table_data += """</table></br></br>"""+get_summary_sheet_abbr_details()+"""</div>"""
            elif head_tracker > 10:
                 table_data += """</table></div></br></br>""" 
                 table_data +=get_page_header(request,prev_level)+get_summary_sheet_abbr_details()+"""</table></div>"""
        # if main_index == 4:
        #     break
    t = Template(table_data)
    c = Context({'test':stud_reg_sum})
    return t.render(c)


def get_summary_table_2(cur_prev_result,courses_from_reg,courses_from_curr,prev_level,request):
    table_data = ''
    table_data += get_page_header(request,prev_level)
    head_tracker = 0
    sn = 0
    for main_index, stud in enumerate(cur_prev_result, start=1):
        head_tracker +=1
        if main_index == 1:
                table_data +=  get_static_table_header_for_summary_sheet()
        firstName = stud['firstname'].split(' ') 
        val_prepare_get_values_for_summary_sheet = prepare_get_values_for_summary_sheet_2(stud['sub'].all(),courses_from_reg,courses_from_curr,request,stud)
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
                table_data +=get_page_header(request,prev_level)+get_static_table_header_for_summary_sheet()
                head_tracker = 0
        if main_index == len(cur_prev_result):
            if head_tracker <= 10:
                table_data += """</table></br></br>"""+get_summary_sheet_abbr_details()+"""</div>"""
            elif head_tracker > 10:
                 table_data += """</table></div></br></br>""" 
                 table_data +=get_page_header(request,prev_level)+get_summary_sheet_abbr_details()+"""</table></div>"""
        # if main_index == 4:
        # break
    t = Template(table_data)
    c = Context({'test':cur_prev_result})
    return t.render(c)

    
def get_broadsheet_table(stud_reg, unique_courses, course_desc,prev_level, request):
    unique_courses_header = get_formatted_header_query(unique_courses)
    str_table = ''
    str_table += get_page_header(request,prev_level)
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
                    str_table +=get_page_header(request,prev_level)+"""<table class="result_table">"""+get_table_header_row(unique_courses_header)
                head_tracker = 0
        # if (len(stud_reg)-main_index) < 20 :
        #     if head_tracker <= 10:
        #         str_table += """</table></br></br>"""+get_unique_courses_desc(course_desc)+"""</div>"""
        #     elif head_tracker > 10:
        #          str_table += """</table></div></br></br>""" 
        #          str_table +=get_page_header(request)+get_unique_courses_desc(course_desc)+"""</table></div>"""
        if len(stud_reg)  == main_index :
                str_table += """</table></div></br></br>""" 
                str_table +=get_page_header(request,prev_level)+get_unique_courses_desc(course_desc)+"""</table></div>"""
    str_table += "</table>" 
    t = Template(str_table)
    c = Context({'test':stud_reg})
    return t.render(c)









