from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import Template,Context
from django.db.models import Q,Prefetch
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from collections import Counter
from django.contrib.auth.decorators import login_required
from undergraduate.models import Course,Curriculum,LecturerCourse,Student
from users.models import User
from base.models import Setting
from base.baseHelper import session_semester_config, session_semester_config_always
from undergraduate.models import Course, Curriculum,Department,Programme,Faculty,RegSummary,Registration
from datetime import datetime



@login_required(login_url='index')
def get_print_result_view(request):
    
    if request.user.user_roles_hod:
        print("HOD @@@@@@@@@@@@@@@@@@@@@@@@@")
        pass
    sessions = Setting.objects.all().distinct('session').order_by('-session')

    return render(request, 'result/printResults.html',{'sessions':sessions})




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
    # params = {'session_id':'2022/2023','semester':'2', 'prog':'CMP', 'level':'300'}
    params = {'session_id':'2021/2022','semester':'1', 'prog':'ECO', 'level':'300'}
    
    session_list = [request.POST.get('session')]
    val1 = request.POST.get('session').split('/')
    current_session = session_semester_config().session.split('/')
    prev_level = int(current_session[1]) - int(val1[1])
    prev_session = f'{str(int(val1[0])-1)}/{str(int(val1[1])-1)}'
    if params['semester'] == '1':
        session_list.append(prev_session)
    stud_reg_sum = [{'matric_number':row.matric_number,
    'surname':row.surname, 'firstname':row.firstname,'summary':row.ug_reg_sum_related.all()} 
    for row in Student.objects.prefetch_related(Prefetch('ug_reg_sum_related'
    ,queryset=RegSummary.objects.filter(session_id__in=session_list))).filter(prog_code= params['prog'],
    current_level=params['level'],status='CURRENT').order_by('matric_number') 
    if [True for val in row.ug_reg_sum_related.all() if val.session_id in session_list ]]

    courses_from_reg = Registration.objects.filter(session_id__lte=request.POST.get('session'), status = 'C',
    matric_number_fk__in=[mats['matric_number'] for mats in stud_reg_sum]).values('matric_number_fk',
    'course_code','score','status','grade')
  
    courses_from_curr = Curriculum.objects.filter(programme=params['prog'],status ='C', course_reg_level__lte= str(prev_level)+'00').values('course_code')
    
    return render(request, 'user/master_sheet_summary.html', context={'data':get_summary_table(stud_reg_sum,courses_from_reg,courses_from_curr,current_session,request)})

def format_level_supplied(param):
    new_level = param
    if param.endswith('+') or param.endswith('F'):
        new_level = param[:-1]
    return int(new_level)

def validate_request_parama(request):
    # if request.POST['summary'] and request.POST['group'] and request.POST['level'] and request.POST['session'] and request.POST['semester']:
    if request.method == 'GET':
        return False
    return True


def get_broadsheet_or_summary_for_print(request):
 
    if validate_request_parama(request):
        get_programme = request.user.programme.programme_code
        session_list = [request.POST.get('session')]
        val1 = request.POST['session'].split('/')
        current_session = session_semester_config().session.split('/')
        prev_level = abs(int(str(int(current_session[1]) - int(val1[1]))+'00') - int(format_level_supplied(request.POST.get('level'))))
        prev_session = f'{str(int(val1[0])-1)}/{str(int(val1[1])-1)}'
        
        if request.POST['to_print'].upper() == 'SUMMARY':
            cur_result = [{'matric_number':row.matric_number,
            'surname':row.surname, 'firstname':row.firstname,'sub':row.ug_reg_stud_related.all()} 
                for row in Student.objects.prefetch_related(Prefetch('ug_reg_stud_related'
            ,queryset=Registration.objects.filter(session_id=request.POST.get('session'), deleted='N', semester=request.POST.get('semester')))
            ).filter(prog_code=get_programme,
            current_level=request.POST.get('level'),status=request.POST.get('group').upper()).order_by('matric_number')
            if row.ug_reg_stud_related.all().count()>0]
           
            cur_prev_result = [{'matric_number':row.matric_number,
            'surname':row.surname, 'firstname':row.firstname,'sub':row.ug_reg_stud_related.all()} 
                for row in Student.objects.prefetch_related(Prefetch('ug_reg_stud_related'
            ,queryset=Registration.objects.filter(session_id__lte=request.POST.get('session'), deleted='N'))
            ).filter(prog_code=get_programme,
            current_level=request.POST.get('level'),status=request.POST.get('group').upper(),
            matric_number__in=[mats['matric_number'] for mats in cur_result]).order_by('matric_number')
            if row.ug_reg_stud_related.all().count()>0]
        
            courses_from_reg = Registration.objects.filter(session_id__lte=request.POST.get('session'), deleted='N', status = 'C',
            matric_number_fk__in=[mats['matric_number'] for mats in cur_result]).values('matric_number_fk',
            'course_code','score','status','grade')
        
            courses_from_curr = Curriculum.objects.filter(programme=get_programme,status ='C', course_reg_level__lte= f'"{prev_level}"').values('course_code')
            list_all_course_code_and_equivalence = [{'course_code':course_row['course_code'],'eqv':course_row['course_id_of_equivalence']} for course_row in Course.objects.all().exclude(course_id_of_equivalence=0).values('course_code','course_id_of_equivalence')]
            
            return render(request, 'user/master_sheet_summary.html', context={'data':get_summary_table_2(cur_prev_result,courses_from_reg,courses_from_curr,prev_level,list_all_course_code_and_equivalence,request)})
        
        elif request.POST['to_print'].upper() == 'BROADSHEET':
               stud_reg = [{'matric_number':row.matric_number,
                'surname':row.surname, 'firstname':row.firstname,'sub':row.ug_reg_stud_related.all()} 
                    for row in Student.objects.prefetch_related(Prefetch('ug_reg_stud_related'
                ,queryset=Registration.objects.filter(session_id=request.POST.get('session'), semester=request.POST.get('semester'), deleted='N')
                )).filter(prog_code=get_programme,current_level=request.POST.get('level'),status=request.POST.get('group').upper()).order_by('matric_number')
                if row.ug_reg_stud_related.all().count()>0]
                
               unique_courses = Registration.objects.filter(session_id=request.POST.get('session'), deleted='N', semester=request.POST.get('semester'),
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



def display_class_master_sheet_summary_exam_direct_from_reg_table(request):
    # params = {'session_id':'2022/2023','semester':'2', 'prog':'CMP', 'level':'300'}
    params = {'session_id':'2021/2022','semester':'1', 'prog':'CMP', 'level':'400'}
    session_list = [request.POST.get('session')]
    val1 = request.POST.get('session').split('/')
    current_session = session_semester_config().session.split('/')
    prev_level = int(current_session[1]) - int(val1[1])
    prev_session = f'{str(int(val1[0])-1)}/{str(int(val1[1])-1)}'
    current_session = session_semester_config().session.split('/')

    cur_result = [{'matric_number':row.matric_number,
    'surname':row.surname, 'firstname':row.firstname,'sub':row.ug_reg_stud_related.all()} 
        for row in Student.objects.prefetch_related(Prefetch('ug_reg_stud_related'
    ,queryset=Registration.objects.filter(session_id=request.POST.get('session'), deleted='N'))).filter(prog_code=params['prog'],
    current_level=params['level'],status='CURRENT').order_by('matric_number')
    if row.ug_reg_stud_related.all().count()>0]

    cur_prev_result = [{'matric_number':row.matric_number,
    'surname':row.surname, 'firstname':row.firstname,'sub':row.ug_reg_stud_related.all()} 
        for row in Student.objects.prefetch_related(Prefetch('ug_reg_stud_related'
    ,queryset=Registration.objects.filter(session_id__lte=request.POST.get('session'), deleted='N'))).filter(prog_code=params['prog'],
    current_level=params['level'],status='CURRENT',
    matric_number__in=[mats['matric_number'] for mats in cur_result]).order_by('matric_number')
    if row.ug_reg_stud_related.all().count()>0]
    
    # return render(request, 'user/master_sheet_summary_2.html', context={'data':cur_result})

    courses_from_reg = Registration.objects.filter(session_id__lte='2021/2022', status = 'C',
    matric_number_fk__in=[mats['matric_number'] for mats in cur_result]).values('matric_number_fk',
    'course_code','score','status','grade')
  
    courses_from_curr = Curriculum.objects.filter(programme=params['prog'],status ='C', course_reg_level__lte= str(prev_level)+'00').values('course_code')
    
   
    return render(request, 'user/master_sheet_summary.html', context={'data':get_summary_table_2(cur_prev_result,cur_result,courses_from_reg,courses_from_curr,current_session,request,params)})



def prepare_get_values_for_summary_sheet_2(subjects,courses_from_reg, courses_from_curr,list_all_course_code_and_equivalence,request,stud,class_performance_summary_dic):
    t_str = ''
    t_str +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str(get_prev_ctnur(subjects, session=request.POST.get('session'),semester=request.POST.get('semester'))) + """</td> """
    t_str +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str(get_prev_ctnup(subjects, session=request.POST.get('session'),semester=request.POST.get('semester'))) + """</td> """
    t_str +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str(get_prev_ctcp(subjects, session=request.POST.get('session'),semester=request.POST.get('semester'))) + """</td> """
    t_str +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str(get_prev_cgpa(get_prev_ctnur(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')), get_prev_ctcp(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')))) + """</td> """
    
    t_str +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str(get_cur_ctnur(subjects, session=request.POST.get('session'),semester=request.POST.get('semester'))) + """</td> """
    t_str +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str(get_cur_ctnup(subjects, session=request.POST.get('session'),semester=request.POST.get('semester'))) + """</td> """
    t_str +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str(get_cur_ctcp(subjects, session=request.POST.get('session'),semester=request.POST.get('semester'))) + """</td> """
    t_str +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str(get_cur_gpa( get_cur_ctnur(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')), get_cur_ctcp(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')) ) ) + """</td> """
    t_str +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+str(get_stud_oustanding_2(stud, courses_from_reg, courses_from_curr,list_all_course_code_and_equivalence, request)[0]) +"""</td>"""
    
    t_str +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str(format_for_str_issue(get_prev_ctnur(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')), get_cur_ctnur(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')))) + """</td> """
    t_str +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str( format_for_str_issue(get_prev_ctnup(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')) , get_cur_ctnup(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')))) + """</td> """
    t_str +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str( format_for_str_issue(get_prev_ctcp(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')) , get_cur_ctcp(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')))) + """</td> """
    t_str +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str(get_cgpa(
        get_prev_ctnur(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')),
        get_prev_ctcp(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')),
        get_cur_ctnur(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')),
        get_cur_ctcp(subjects, session=request.POST.get('session'),semester=request.POST.get('semester'))
    )) + """</td> """
    t_str +="""<td style="text-align:left;width:25px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+str(get_stud_oustanding_2(stud, courses_from_reg, courses_from_curr,list_all_course_code_and_equivalence, request)[1]) +"""</td>"""
    t_str +="""<td   style="text-align: left;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+str(get_acad_status(get_cgpa(
        get_prev_ctnur(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')),
        get_prev_ctcp(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')),
        get_cur_ctnur(subjects, session=request.POST.get('session'),semester=request.POST.get('semester')),
        get_cur_ctcp(subjects, session=request.POST.get('session'),semester=request.POST.get('semester'))
    ),class_performance_summary_dic))+"""</td>"""
    
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

def get_prev_ctcp(courses,session, semester):
    prev_ctcp = 0
    for row in courses:
        if  row.session_id < session and row.score != -1:
            prev_ctcp += int(row.unit) * int(get_point_from_score(row.score))
    if semester == '2':
        for row in courses:
            if  row.session_id == session and row.semester == '1' and row.score != -1:
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



def get_prev_ctnup(courses,session, semester):
    prev_ctnup = 0
    for row in courses:
        if row.score >= 40 and row.session_id < session:
            prev_ctnup += int(row.unit)
    if semester == '2':
        for row in courses:
            if row.score >= 40 and row.session_id == session and row.semester == '1':
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

def get_prev_ctnur(courses, session, semester):
    prev_ctnur = 0
    for row in courses:
        if row.session_id < session and row.score != -1:
            prev_ctnur += int(row.unit)
    if semester == '2':
         for row in courses:
            if row.session_id == session and row.semester=='1' and row.score != -1:
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

def get_acad_status(cgpa,class_performance_summary_dic):
    
    if isinstance(cgpa, str):
        return 'None'
    cgpa = round(cgpa,2)
    if cgpa >= 4.50:
        class_performance_summary_dic['first_class'] = int(class_performance_summary_dic['first_class']+1)
        return 'GSD (Excellent)'
    elif  cgpa >= 3.50 and cgpa <= 4.49:
        class_performance_summary_dic['second_class_upper'] = int(class_performance_summary_dic['second_class_upper']+1)
        return 'GSD (V. Good)'
    elif  cgpa >= 2.50 and cgpa <= 3.49:
        class_performance_summary_dic['second_class_lower'] = int(class_performance_summary_dic['second_class_lower']+1)
        return 'GSD (Good)'
    elif  cgpa >= 1.50 and cgpa <= 2.49:
        class_performance_summary_dic['third_class'] = int(class_performance_summary_dic['third_class']+1)
        return 'GSD (Average)'
    elif  cgpa >= 1.00 and cgpa <= 1.49:
        class_performance_summary_dic['pass'] = int(class_performance_summary_dic['pass']+1)
        return 'PRB (Fair)'
    elif  cgpa < 1.00 :
        class_performance_summary_dic['poor'] = int(class_performance_summary_dic['poor']+1)
        return 'WRN (V. Poor)'


def prepare_get_values_for_summary_sheet(summary_instance,courses_from_reg, courses_from_curr,request):
    params = {'session_id':'2021/2022','semester':'1', 'prog':'ECO', 'level':'300'}
    t_str = ''
    prev = {}
    curr = list(filter(lambda row:row.session_id == request.POST.get('session') and row.semester == params['semester'], summary_instance))
    if params['semester'] == '2':
        prev = list(filter(lambda row:row.session_id == request.POST.get('session') and row.semester == '1', summary_instance))
    elif params['semester'] == '1':
        prev_session_list = request.POST.get('session').split('/')
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


def get_stud_oustanding_2(stud,courses_from_reg,courses_from_curr,list_all_course_code_and_equivalence, request):
    
    list_reg_courses = [row['course_code'] for row in courses_from_reg 
                    if row['matric_number_fk'] == f"{stud['matric_number']}"]

    list_reg_failed_courses = [row['course_code'] for row in courses_from_reg 
                if row['matric_number_fk'] == f"{stud['matric_number']}" and row['grade']=='F']
    
    list_reg_pass_courses = [row['course_code'] for row in courses_from_reg 
                if row['matric_number_fk'] == f"{stud['matric_number']}" and row['grade']!='F']

    list_curr_courses = [row['course_code'] for row in courses_from_curr]
    # for rec in list_all_course_code_and_equivalence:
    #     if rec['eqv'] == 0:
    #         print(rec)

    courses_in_curr_not_reg = list((Counter(list_curr_courses) - Counter(list_reg_courses)).elements())

    # if len(courses_in_curr_not_reg) > 0:
          
    #       courses_in_curr_not_reg = [f'*{course}' for course in courses_in_curr_not_reg]
    courses = ''
    combined = list_reg_failed_courses + courses_in_curr_not_reg
    for course_code in combined:
        filter1 = list(filter(lambda row:row['course_code'] == course_code, list_all_course_code_and_equivalence))
        if len(filter1) >0: 
             filter2 = list(filter(lambda row:row['eqv'] == filter1[0]['eqv'], list_all_course_code_and_equivalence))
             list_eqv_course_code = [item['course_code'] for item in filter2]
             for course in list_eqv_course_code:
                if course in list_reg_pass_courses:
                    for course_2 in list_eqv_course_code:
                        if course_2 in combined:
                            combined.remove(course_2)
             
    for index, course in enumerate(combined, start=1):
        courses += course
        if index != len(combined):
            courses += ' , '
            if index == 6:
                courses += ' ...'
                break
    return [len(combined),courses]


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
        if courses_score_dic[course['course_code']] == -1:
            return 'r'
        else: return courses_score_dic[course['course_code']]
     return ''

def get_table_header_row(unique_courses_header):      
       table_header = """<tr >
       <th style="text-align: center;width:2px;height: 5px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;"> SN</th>
       <th style="text-align: center;width:18px;height: 5px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">Matric Number</th>
       <th style="text-align: center;width:20px;height: 5px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">Names</th>
       <th style="text-align: center;width:3px;height: 5px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">TUR</th>
        """
       for obj in unique_courses_header:
           table_header+= """<th  style="text-align: center;height: 20px;padding:0px;margin:0;overflow:hidden;white-space:nowrap;">
            <div  >"""+  str(obj['course_code'])+"""
            <h6 style="white-space:nowrap;padding:1px;margin:0;"> """+ str(obj['unit'])+"""</h6>
            <h6>""" +str(obj['status']) +"""</h6>
            </div></th>"""
       table_header += """</tr>"""
       return table_header


def get_page_header(request, prev_level):
    
    faculty = Faculty.objects.filter(id = request.user.faculty.id).first().faculty if Faculty.objects.filter(id = request.user.faculty.id).first().faculty else " "
    dept = Department.objects.filter(id = request.user.department.id).first().department if Department.objects.filter(id = request.user.department.id).first().department else " "
    prog = Programme.objects.filter(programme_code = request.user.programme.programme_code).first().programme if Programme.objects.filter(programme_code = request.user.programme.programme_code).first().programme else " "
  
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

def get_summary_sheet_abbr_details(class_performance_summary_dic):
    return """
        <table ><tr> <td> 
        <table width="30%" class="result_table2" style="display:inline-table;">
            <tr><span style="margin-left: 5%;">Class Performance Summary</span></tr>
            <tr>
                <td>1st Class</td>
                <td>2nd Class Upper</td>
                <td>2nd Class Lower</td>
                <td>3rd Class </td>
                <td>Pass </td>
                <td>Poor </td>
                <td>Non Grad </td>
            </tr>
            <tr>
                <td>"""+ str(class_performance_summary_dic['first_class']) +"""</td>
                <td>"""+ str(class_performance_summary_dic['second_class_upper']) +"""</td>
                <td>"""+ str(class_performance_summary_dic['second_class_lower']) +"""</td>
                <td>"""+ str(class_performance_summary_dic['third_class']) +"""</td>
                <td>"""+ str(class_performance_summary_dic['pass']) +"""</td>
                <td>"""+ str(class_performance_summary_dic['poor']) +"""</td>
                <td>"""+ str(class_performance_summary_dic['non_grad']) +"""</td>
            </tr>
         
        </table></td>

        <td><table width="30%" class="result_table2" style="display:inline-table;">
            <tr><span style="margin-left: 5%;">INTERPRETATION OF TERMS</span></tr>
           <tr>
                <td>TNUR = Total Number of Units Registered</td>
                   
           </tr>
           <tr>
                <td>TCP = Total Credit Point</td>
                   
           </tr>
           <tr>
                <td>TNUP = Total Number of Units Passed </td>
                   
           </tr>
           <tr>
                <td>GPA = Grade Point Average</td>
                   
           </tr>
           <tr>
                <td>GSD = Good Standing</td>
                   
           </tr>
           <tr>
                <td>PRB = Probation</td>
                   
           </tr>
           <tr>
                <td>WRN = Warning</td>
                   
           </tr>
           <tr>
                <td>WDL = Withdrawal</td>
                   
           </tr>
         
        </table>
            
        </td>
        
         </tr> 
         
         <tr> 
            <td>
             <table  class="result_table2" style="display:inline-table;">
            <tr>
                <td style="border:0;">   <pre>
            Head of Department                    Dean                                  External Examiner
            Name: _____________________           Name:_____________________            Name:_____________________

            Sign: _____________________           Sign:_____________________            Sign:_____________________

            Date: _____________________           Date:_____________________            Date:_____________________
            </pre></td>
            </tr>
            </table>
             </td>
         </tr>
          </table>

           
       
        <div class="print_footer">
            Generated on the """ + str(datetime.now()) + """<br><br>
        </div>
    </div> """


def get_summary_table(stud_reg_sum,courses_from_reg,courses_from_curr,prev_level,request):
    table_data = ''
    table_data += get_page_header(request,prev_level)
    class_performance_summary_dic = {'first_class':0, 'second_class_upper':0, 'second_class_lower':0,'third_class':0,'pass':0,'poor':0,'non_grad':0}
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
                table_data += """</table></br></br>"""+get_summary_sheet_abbr_details(class_performance_summary_dic)+"""</div>"""
            elif head_tracker > 10:
                 table_data += """</table></div></br></br>""" 
                 table_data +=get_page_header(request,prev_level)+get_summary_sheet_abbr_details(class_performance_summary_dic)+"""</table></div>"""
        # if main_index == 4:
        #     break
    t = Template(table_data)
    c = Context({'test':stud_reg_sum})
    return t.render(c)


def get_summary_table_2(cur_prev_result,courses_from_reg,courses_from_curr,prev_level,list_all_course_code_and_equivalence,request):
    table_data = ''
    class_performance_summary_dic = {'first_class':0, 'second_class_upper':0, 'second_class_lower':0,'third_class':0,'pass':0,'poor':0,'non_grad':0}
    table_data += get_page_header(request,prev_level)
    head_tracker = 0
    last_index = 0
    sn = 0
    for main_index, stud in enumerate(cur_prev_result, start=1):
        if main_index > last_index:
            last_index = main_index
        head_tracker +=1
        if main_index == 1:
                table_data +=  get_static_table_header_for_summary_sheet()
        firstName = stud['firstname'].split(' ') 
        val_prepare_get_values_for_summary_sheet = prepare_get_values_for_summary_sheet_2(stud['sub'].all(),courses_from_reg,courses_from_curr,list_all_course_code_and_equivalence,request,stud,class_performance_summary_dic)
        if val_prepare_get_values_for_summary_sheet == '':
            continue
        sn +=1
        table_data += """<tr><td>"""+ str(sn) + """</td>
         <td>"""+ stud['matric_number'] + """</td>
         <td style="text-align: left;width: 20px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;"> """+ stud['surname'] + """   """+firstName[0] +"""</td>
         """+val_prepare_get_values_for_summary_sheet+"""
         </tr>"""
        if head_tracker == 25 and main_index != len(cur_prev_result):
                table_data += """</table></div></br></br>""" 
                table_data +=get_page_header(request,prev_level)+get_static_table_header_for_summary_sheet()
                head_tracker = 0
        if len(cur_prev_result) == last_index: 
            if head_tracker <= 15:
                table_data += """</table></br></br>"""+get_summary_sheet_abbr_details(class_performance_summary_dic)+"""</div>"""
            elif head_tracker > 15:
                 table_data += """</table></div></br></br>""" 
                 table_data +=get_page_header(request,prev_level)+get_summary_sheet_abbr_details(class_performance_summary_dic)+"""</table></div>"""
       
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
    last_index = 0
    for main_index, stud in enumerate(stud_reg, start=1): 
        if main_index > last_index:
            last_index = main_index
        tur = str(get_total_unit_reg_in_semester(stud['sub']) )
        if main_index == 1:
                str_table += """<table class="result_table" >"""
                str_table +=get_table_header_row(unique_courses_header)
        head_tracker +=1
        # style="width: 20px;height: 40px" [: (len(firstName[0])-10)]
        
        firstName = stud['firstname'].split(' ')
        courses_score_dic = get_all_courses_in_dic(stud['sub'])
        str_table += """ <tr >
    <td style="text-align: left;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str(main_index) +"""</td>
    <td style="text-align: center;width:18px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ stud['matric_number'] +"""</td>
    <td style="text-align: left;width: 20px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ stud['surname']+"""  """ +firstName[0]+"""</td>
    <td style="text-align: center;width:3px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+tur+"""</td>"""
        for ind,course in enumerate(unique_courses_header):
            str_table +="""<td style="text-align: center;width:2px;height: 20px;padding:0px 0px 0px 0px;overflow:hidden;white-space:nowrap;">"""+ str(get_score_for_current_course_header(courses_score_dic,course))+"""</td>""" 
        
        str_table += """</tr> """  
        
        if head_tracker == 25 and main_index != len(stud_reg) :
                str_table += """</table></div></br></br>"""
                str_table +=get_page_header(request,prev_level)+"""<table class="result_table">"""+get_table_header_row(unique_courses_header)
                head_tracker = 0
        if len(stud_reg)  == last_index:
            if head_tracker <= 10:
                str_table += """</table></br></br>"""+get_unique_courses_desc(course_desc)+"""</div>"""
            elif head_tracker > 10:
                 str_table += """</table></div></br></br>""" 
                 str_table +=get_page_header(request,prev_level)+get_unique_courses_desc(course_desc)+"""</table></div>"""
       
        # if len(stud_reg)  == last_index :
        #     if head_tracker <= 5:
        #         str_table += """</table></div></br></br>""" 
        #         str_table +=get_page_header(request,prev_level)+get_unique_courses_desc(course_desc)+"""</table></div>"""
    
    
    str_table += "</table>" 
    t = Template(str_table)
    c = Context({'test':stud_reg})
    return t.render(c)









