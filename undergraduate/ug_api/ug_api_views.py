# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.decorators import  api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from base.models import Setting,Staff
from .ug_serializer import SettingSerializer
from undergraduate.models import Faculty, Department,Programme,Course,Curriculum,Registration,RegSummary,Student
from base.baseHelper import session_semester_config, session_semester_config_always
import json
from datetime import datetime

@api_view(['GET', 'POST'])
def correct_prog_dpt_diff(request):
    with open("C:/Users/PC/Downloads/t_departments (1).json") as f:
        records = json.load(f)
    for record in records:
        dpt = Department.objects.filter(department=record['department']).first()
        prog = Programme.objects.filter(programme_id=record['programme_id']).first()
        prog.department_id = dpt.id
        prog.save()
        
    return Response({'data':records})


# @login_required(login_url='index')
@api_view(['GET', 'POST'])
def loadRegistrationsJson(request):   
    # return Response({'data':''}) 
    # with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/t_registrations.json") as f:
    jamb_no_list = []
    with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/t_registrations.json") as f:
        records = json.load(f)
        settings = session_semester_config()
        reg_list = [Registration(
        matric_number_fk= reg['s_matric_number'],course_code = reg['s_course_code'],
        semester = settings.semester_code,session_id = settings.session, unit = reg['s_course_unit'],
        score = -1, status = reg['s_course_status'] ,level = reg['registration_level'],unit_id = reg['s_course_id'].split('*')[1]
        )
         for reg in records[:1]]
        bulk_create = Registration.objects.bulk_create(reg_list, ignore_conflicts=True)
        # new_data_list = []
        # for item in bulk_create:
        #     filter_list = list(filter(lambda row:row['matric_number'] == item.matric_number_fk , new_data_list))
        #     if len(filter_list)>0:
        #         filter_list[0]['courses_taken'] = int(filter_list[0]['courses_taken'])+ 1
        #         filter_list[0]['tnur'] = int(filter_list[0]['tnur'])+ int(item.unit)
        #         filter_list[0]['ctnur'] = int(filter_list[0]['ctnur'])+ int(item.unit)
        #     else:
        #         new_data_list.append({
        #             'matric_number': item.matric_number_fk,'semester':item.semester,
        #             'session_id' : item.session_id,'courses_taken':1,'courses_passed':0,'courses_failed':0,'tnur':item.unit,'tnup':0,
        #             'tnuf':0,'wcrp':0,'gpa':0,'ctnur':item.unit,'ctnup':0,'cgpa':0,'ctcp':0,'ctcup':0,'cteup':0, 'acad_status':'', })

        # reg_list2 = [RegSummary(
        # matric_number_fk = Student.objects.get(matric_number = stud['matric_number']) ,semester = stud['semester'],
        # session_id = stud['session_id'], courses_taken = stud['courses_taken'],
        # courses_passed = stud['courses_passed'], courses_failed = stud['courses_failed'] ,
        # tnur = stud['tnur'], tnup = stud['tnup'], tnuf = stud['tnuf'],wcrp = stud['wcrp'],gpa = stud['gpa'],
        # ) for stud in new_data_list]
        # bulk_create = RegSummary.objects.bulk_create(reg_list2, ignore_conflicts=True)		
      
        return Response({'data':bulk_create})
    
    return Response({'data':records[0:4]})


# @login_required(login_url='index')
# @api_view(['GET', 'POST'])
# def loadJson(request):    
#     with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/data_export_psql_19_01_2023/dept.json") as f:
#         records = json.load(f)

#     for record in records:   

#         fac = Department( 
#             id = record['id'],
#             department = record['department'],
#             deleted = record['deleted'],
#             created = record['created'],
#             updated = record['updated'],
#             faculty_id = record['faculty_id'],
#             last_updated_by = request.user,
         
#             )
#         fac.save()
#         # return Response({'data':record})
    
#     return Response({'data':records[0:4]})




@login_required(login_url='index')
@api_view(['GET', 'POST'])
def loadJson_prog(request):    
    with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/14_03_2023/backup_prog_from_myself.json") as f:
        records = json.load(f)

    for index,record in enumerate(records, start=1):   

        fac = Programme( 
           id = index,
           programme_code = record['programme_id'] ,
           programme = record['programme'] ,
           department_id =  record['department_id'] ,
           deleted = record['deleted'],
           created = record['created'],
           updated = record['updated'],
           required_ctcup = record['required_ctcup'],
           required_cteup = record['required_cteup'],
           last_updated_by=request.user,
         
            )
        fac.save()
        # return Response({'data':record})
    
    return Response({'data':records[0:4]})







# @api_view(['GET', 'POST'])
# def loadJson(request):   
#     with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/data_export_psql_19_01_2023/staff.json") as f:
#         records = json.load(f)

#     for record in records:   

#         fac = Staff( 
#          id=record['id'],
#          userid=record['userid'],
#          email=record['email'],
#          phone=record['phone'],
#          password=record['password'],
#          profile_image=record['profile_image'],
#          profile_image_small=record['profile_image_small'],
#          staff_type=record['staff_type'],
#          question=record['question'],
#          answer=record['answer'],
#          online=record['online'],
#          activate=record['activate'],
#          pwdreset=record['pwdreset'],
#          lastupdate=record['lastupdate'],
#          form_completed=record['form_completed'],
#          retired=record['retired'],
#          adjunct=record['adjunct'],
#          disengaged=record['disengaged'],
#          reason=record['reason'],
#          r_date=record['r_date'],
#          support_team=record['support_team'],
#          research_output=record['research_output'],
#          phd_output=record['phd_output'],
#          msc_output=record['msc_output'],
#          date=record['date'],
#          c_address=record['c_address'],
#          covenant=record['covenant'],
#          cv=record['cv'],
#          date_app_pubservice=record['date_app_pubservice'],
#          date_app_uni=record['date_app_uni'],
#          dob=record['dob'],
#          email_status=record['email_status'],
#          employment_type=record['employment_type'],
#          firstname=record['firstname'],
#          former_firstname=record['former_firstname'],
#          former_lastname=record['former_lastname'],
#          former_middlename=record['former_middlename'],
#          gender=record['gender'],
#          health=record['health'],
#          hobbies=record['hobbies'],
#          intercom=record['intercom'],
#          ipbirth=record['ipbirth'],
#          istate=record['istate'],
#          landline=record['landline'],
#          lastname=record['lastname'],
#          leave_app=record['leave_app'],
#          middlename=record['middlename'],
#          mobile=record['mobile'],
#          mstatus=record['mstatus'],
#          myprofile=record['myprofile'],
#          nationality=record['nationality'],
#          office_phone=record['office_phone'],
#          p_address=record['p_address'],
#          p_email=record['p_email'],
#          pob=record['pob'],
#          poblga=record['poblga'],
#          r_address=record['r_address'],
#          sh_staff_no=record['sh_staff_no'],
#          signature=record['signature'],
#          staff_no=record['staff_no'],
#          state_origin=record['state_origin'],
#          title=record['title'],
#          user_id=''
#             )
#         # fac.save()
#         return Response({'data':records[0:4]})
    
#     return Response({'data':records[0:4]})




# @login_required(login_url='index')
# @api_view(['GET', 'POST'])
# def loadJson(request):    
#     with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/data_export_psql_19_01_2023/SETTINGS.json") as f:
#         records = json.load(f)

    # for record in records:   

    #     fac = Setting( 
    #         id = record['id'],
    #         session = record['session'],
    #         semester_name = record['semester_name'],
    #         semester_code = record['semester_code'],
    #         status = record['status'],
    #         created = record['created'],
    #         updated = record['updated'],
    #         semester_open_close = False,
         
    #         )
    #     fac.save()
    #     # return Response({'data':record})
    
    # return Response({'data':records[0:4]})




# @login_required(login_url='index')
# @api_view(['GET', 'POST'])
# def loadJson(request):    
#     with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/data_export_psql_19_01_2023/faculty.json") as f:
#         records = json.load(f)

#     for record in records:   

#         fac = Faculty( 
#             id = record['id'],
#             faculty = record['faculty'],
#             deleted = record['deleted'],
#             created = record['created'],
#             updated = record['updated'],
#             last_updated_by_old = 'toyo@gmail.com'  #request.user.email,
         
#             )
#         fac.save()
#         # return Response({'data':record})
    
#     return Response({'data':records[0:4]})


@login_required(login_url='index')
@api_view(['GET', 'POST'])
def loadJson_reg_summary(request):  
    with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/T_REG_SUMMARY.json") as f:
        records = json.load(f)

    
        # regSumList = [RegSummary( 
        #    matric_number_fk =  Student.objects.get(matric_number=record['matric_number'] ) if 'matric_number' in record.keys() else None,
        #    semester = record['semester'] if 'semester' in record.keys() else None,
        #    session_id = record['session_id'] if 'session_id' in record.keys() else None,
        #    courses_taken = record['courses_taken'] if 'courses_taken' in record.keys() else None,
        #    courses_passed = record['courses_passed'] if 'courses_passed' in record.keys() else None,
        #    courses_failed = record['courses_failed'] if 'courses_failed' in record.keys() else None,
        #    tnur = record['tnur'] if 'tnur' in record.keys() else None,
        #    tnup = record['tnup'] if 'tnup' in record.keys() else None,
        #    tnuf = record['tnuf'] if 'tnuf' in record.keys() else None,
        #    ctnur = record['ctnur'] if 'ctnur' in record.keys() else None,
        #    ctnup = record['ctnup'] if 'ctnup' in record.keys() else None,
        #    ctcp = record['ctcp'] if 'ctcp' in record.keys() else None,
        #    ctcup = record['ctcup'] if 'ctcup' in record.keys() else None,
        #    cteup = record['cteup'] if 'cteup' in record.keys() else None,
        #    wcrp = record['wcrp'] if 'wcrp' in record.keys() else None,
        #    gpa = record['gpa'] if 'gpa' in record.keys() else None,
        #    cgpa = record['cgpa'] if 'cgpa' in record.keys() else None,
        #    acad_status = record['acad_status'] if 'acad_status' in record.keys() else None,
        #    last_updated_by_old = record['last_updated_by'] if 'last_updated_by' in record.keys() else None,
        #    last_updated_date_old = record['last_update_date'] if 'last_update_date' in record.keys() else None,
        #    deleted = record['deleted'] if 'deleted' in record.keys() else None,
        #     last_updated_by_new=request.user,
         
        #     ) for record in records]

        # RegSummary.objects.bulk_create(regSumList)  
        
        # return Response({'data':record})
    
    return Response({'data':len(records)})




@login_required(login_url='index')
@api_view(['GET', 'POST'])
def loadJson_reg(request):   
    # return Response({'data':''}) 
    with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/14_03_2023/registration.json") as f:
        records = json.load(f)
    # 525718
        regList = [Registration( 
           matric_number_fk = Student.objects.get(matric_number=record['matric_number'] ) if 'matric_number' in record.keys() else None,
           semester = record['semester'] if 'semester' in record.keys() else None,
           session_id = record['session_id'] if 'session_id' in record.keys() else None,
           course_code = record['course_code'] if 'course_code' in record.keys() else None,
           status = record['status'] if 'status' in record.keys() else None,
           unit = Course.objects.filter(course_code=record['course_code'], unit_id=record['unit_id']
           ).first().unit if Course.objects.filter(course_code=record['course_code'], unit_id=record['unit_id']
           ).first().unit else 0,
           score = record['score'] if 'score' in record.keys() else None,
           grade = record['grade'] if 'grade' in record.keys() else None,
           last_updated_date_old = record['last_update_date'] if 'last_update_date' in record.keys() else None,
           last_updated_by_old = record['last_updated_by'] if 'last_updated_by' in record.keys() else None,
           deleted = record['deleted'] if 'deleted' in record.keys() else None,
           unit_id = record['unit_id'] if 'unit_id' in record.keys() else None,
           app_user_id = record['app_user_id'] if 'app_user_id' in record.keys() else None, 
           last_updated_by_new=request.user,
          ) for record in records]

        Registration.objects.bulk_create(regList)  
    
    return Response({'data':len(records)})


# @login_required(login_url='index')
# @api_view(['GET', 'POST'])
# def loadJson(request):    
#     with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/T_PROG_COURSE.json") as f:
#         records = json.load(f)

#     for record in records:   

#         fac = Curriculum( 
#            programme_id = record['prog_code'],
#            course_code = record['course_code'],
#            status = record['status'],
#            last_updated_by_old = record['last_updated_by'],
#            last_updated_date_old = record['last_update_date'],
#            course_reg_level = record['course_level'],
#            semester = record['semester'],
#            register_flag = record['register_flag'],
           
#             last_updated_by_new=request.user,
         
#             )
#         fac.save()
#         # return Response({'data':record})
    
#     return Response({'data':records[0:4]})




@login_required(login_url='index')
@api_view(['GET', 'POST'])
def loadJson_courses(request):    
    with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/14_03_2023/courses.json") as f:
        records = json.load(f)

    for record in records:   
        fac = Course( 
            course_code = record['course_code'] if 'course_code' in record.keys() else None,
            course_title = record['course_title'] if 'course_title' in record.keys() else None,
            unit = record['unit'] if 'unit' in record.keys() else None,
            last_updated_by_old = record['last_updated_by'] if 'last_updated_by' in record.keys() else None,
            last_update_date = record['last_update_date'] if 'last_update_date' in record.keys() else None,
            deleted = record['deleted'] if 'deleted' in record.keys() else None,
            course_id_of_equivalence = record['eq_class'] if 'eq_class' in record.keys() else None,
            unit_id = record['unit_id'] if 'unit_id' in record.keys() else None,
            status = record['status'] if 'status' in record.keys() else None,
            course_level = record['course_level'] if 'course_level' in record.keys() else None,
            last_updated_by_new=request.user,
         
            )
        fac.save()
        # return Response({'data':record})
    
    return Response({'data':records[0:4]})


@login_required(login_url='index')
@api_view(['GET', 'POST'])
def loadJson_cur(request):    
       with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/14_03_2023/curriculum.json") as f:
        records = json.load(f)

        for index, record in enumerate(records, start=1):   

            fac = Curriculum( 
            programme = Programme.objects.filter(programme_code = record['prog_code']).first(),
            course_code = record['course_code'],
            status = record['status'],
            last_updated_by_old = record['last_updated_by'],
            last_updated_date_old = record['last_update_date'],
            course_reg_level = record['course_level'],
            semester = record['semester'],
            register_flag = record['register_flag'],
            last_updated_by_new=request.user,
            
                )
            fac.save()
            # return Response({'data':record})
       
    
        return Response({'data':records[0:4]})






@login_required(login_url='index')
@api_view(['GET', 'POST'])
def loadJson_student(request):    
    with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/T_STUDENT.json") as f:
        records = json.load(f)

    
    # studList = [Student(
    #     matric_number=record['matric_number'] if 'matric_number' in record.keys() else None,
    #     surname=record['surname'] if 'surname' in record.keys() else None,
    #     firstname=record['firstname'] if 'firstname' in record.keys() else None,
    #     sex=record['sex'] if 'sex' in record.keys() else None,
    #     current_level=record['current_level'] if 'current_level' in record.keys() else None,
    #     programme=record['programme'] if 'programme' in record.keys() else None,
    #     status=record['status'] if 'status' in record.keys() else None,
    #     last_updated_by_old=record['last_updated_by'] if 'last_updated_by' in record.keys() else None,
    #     last_update_date_old=record['last_update_date'] if 'last_update_date' in record.keys() else None,
    #     deleted=record['deleted'] if 'deleted' in record.keys() else None,
    #     ctcp=record['ctcp'] if 'ctcp' in record.keys() else None,
    #     ctnur=record['ctnur'] if 'ctnur' in record.keys() else None,
    #     ctnup=record['ctnup'] if 'ctnup' in record.keys() else None,
    #     ctnuf=record['ctnuf'] if 'ctnuf' in record.keys() else None,
    #     cgpa=record['cgpa'] if 'cgpa' in record.keys() else None,
    #     ctcup=record['ctcup'] if 'ctcup' in record.keys() else None,
    #     cteup=record['cteup'] if 'cteup' in record.keys() else None,
    #     gpa= record['gpa'] if 'gpa' in record.keys() else None,
    #     prog_code=record['prog_code'] if 'prog_code' in record.keys() else None,
    #     notify_sms=record['notify_sms'] if 'notify_sms' in record.keys() else None,
    #     notify_email=record['notify_email'] if 'notify_email' in record.keys() else None,
    #     parent_pwd=record['parent_pwd'] if 'parent_pwd' in record.keys() else None,
    #     registration_pwd=record['registration_pwd'] if 'registration_pwd' in record.keys() else None,
    #     financial_flag=record['financial_flag'] if 'financial_flag' in record.keys() else None,
    #     notify_bursary_sms=record['notify_bursary_sms'] if 'notify_bursary_sms' in record.keys() else None,
    #     hold_record=record['hold_record'] if 'hold_record' in record.keys() else None,
    #     birth_date=record['birth_date'] if 'birth_date' in record.keys() else None,
    #     address=record['address'] if 'address' in record.keys() else None,
    #     email1=record['email1'] if 'email1' in record.keys() else None,
    #     email2=record['email2'] if 'email2' in record.keys() else None,
    #     student_phone=record['student_phone'] if 'student_phone' in record.keys() else None,
    #     parent_phone=record['parent_phone'] if 'parent_phone' in record.keys() else None,
    #     jamb_reg=record['jamb_reg'] if 'jamb_reg' in record.keys() else None,
    #     acad_status=record['acad_status'] if 'acad_status' in record.keys() else None,
    #     entry_mode=record['entry_mode'] if 'entry_mode' in record.keys() else None,
    #     lga=record['lga'] if 'lga' in record.keys() else None,
    #     state_origin=record['state_origin'] if 'state_origin' in record.keys() else None,
    #     country=record['country'] if 'country' in record.keys() else None,
    #     city_resident=record['city_resident'] if 'city_resident' in record.keys() else None,
    #     state_resident=record['state_resident'] if 'state_resident' in record.keys() else None,
    #     matric_date=record['matric_date'] if 'matric_date' in record.keys() else None,
    #     graduation_date=record['graduation_date'] if 'graduation_date' in record.keys() else None,
    #     picture=record['picture'] if 'picture' in record.keys() else None,
    #     run_mail=record['run_mail'] if 'run_mail' in record.keys() else None,
    #     degree_sought=record['degree_sought'] if 'degree_sought' in record.keys() else None,
    #     run_mail_2=record['run_mail_2'] if 'run_mail_2' in record.keys() else None,
    #     last_updated_by_new=request.user,
        
    #     ) for record in records]

    # Student.objects.bulk_create(studList)   
        # return Response({'data':record})
    
    return Response({'data':len(records)})



class SettingApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        # setting = Setting.objects.filter(user = request.user.id)
        # setting = Setting.objects.filter(status='ACTIVE').first()
        setting = Setting.objects.all()
        serializer = SettingSerializer(setting, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    # def post(self, request, *args, **kwargs):
    #     '''
    #     Create the Todo with given todo data
    #     '''
    #     data = {
    #         'task': request.data.get('task'), 
    #         'completed': request.data.get('completed'), 
    #         'user': request.user.id
    #     }
    #     serializer = TodoSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



