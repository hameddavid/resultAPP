from django.http import HttpResponse, JsonResponse
from django.template import  Context
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from base.models import Staff
from users import helpers
from base.baseHelper import session_semester_config, session_semester_config_always, check_network
from users.userForm import UserForm
from users.models import User
from course.models import LecturerCourse,Course
import json, os, re,random,string
from django.forms.models import model_to_dict
from undergraduate.models import Course, Curriculum,Student,Department,Programme,RegSummary,Registration
from collections import Counter
from rest_framework import status, generics

from django.db import connection
from django.core.mail import send_mail
from django.conf import settings





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


    # table_name = "ug_programmes"
    # sequence_name = f"{table_name}_id_seq"
    # with connection.cursor() as cursor:
    #     cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1;")
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
                            if  f'{session_semester_config().id}' not in user.role.keys():
                                print(f"{user.role.keys()} in")
                                user.role[session_semester_config().id] = []
                                user.save()
                            request.session['settings'] = model_to_dict(session_semester_config())
                            # Lecturer courses for this semester
                            request.session['pendCourses'] = LecturerCourse.objects.filter(Q(lecturer=request.user) & Q(status=0)).count()
                            request.session['appCourses'] = LecturerCourse.objects.filter(Q(lecturer=request.user) & Q(status=10)).count()
                            
                            # return redirect('dashboard')
                            return JsonResponse({'data':'','status':'success','message':'Login successful!'}, safe=False, status=status.HTTP_200_OK)
                        else:
                            return JsonResponse({'data':'','status':'Failed','message':'Invalid username/password (or inactive account)'}, safe=False, status=status.HTTP_400_BAD_REQUEST)

                    else:
                        # messages.error(request, )
                        user.otp = unique_user_otp_generator(6)
                        user.save()
                        if check_network():
                            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                            print(helpers.send_email(user))
                            # helpers.semester_activation_email(user)
                        else:
                            return JsonResponse({'data':'','status':'Failed','message':"No internet available to send you OTP, kindly connect to one"}, safe=False, status=status.HTTP_200_OK)
                        # return redirect('semester_activation')
                        return JsonResponse({'url':'otp','data':'','status':'success','message':f"Kindly activate your account for {session_semester_config().semester_name} {session_semester_config().session} academic session"}, safe=False, status=status.HTTP_200_OK)
            else:
                staff = Staff.objects.filter(email=email).first()
                if staff is not None:
                    save_user = User.objects.create_user(email = email, password =password,is_active = False, semester_session_id=session_semester_config(),otp=unique_user_otp_generator(6))
                    save_user.save()
                    if check_network():
                        helpers.send_email(user)
                        # helpers.semester_activation_email(user)
                    else:
                        return JsonResponse({'data':'','status':'Failed','message':"No internet available to send you OTP, kindly connect to one"}, safe=False, status=status.HTTP_200_OK)
                    # return redirect('otp')
                    return JsonResponse({'url':'otp','data':'','status':'success','message':f"Kindly activate your account for {session_semester_config().semester_name} {session_semester_config()} academic session"}, safe=False, status=status.HTTP_200_OK)

                else:
                    return JsonResponse({'data':'','status':'Failed','message':'Wrong staff email supplied'}, safe=False, status=status.HTTP_400_BAD_REQUEST)

        else:
            return JsonResponse({'data':'','status':'Failed','message': "No active session/semester, contact Admin"}, safe=False, status=status.HTTP_400_BAD_REQUEST)

            
    except:
        return JsonResponse({'data':'','status':'Failed','message': "User does not exist (catch)"}, safe=False, status=status.HTTP_400_BAD_REQUEST)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='index')
def dashboard(request):
    
    context = {'prog':Programme.objects.all(),'dpt':Department.objects.all()}
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