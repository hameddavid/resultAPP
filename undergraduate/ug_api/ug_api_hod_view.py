from rest_framework.views import APIView
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import  api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions,authentication
from rest_framework import status, generics
from django.db.models import Prefetch
from base.baseHelper import session_semester_config, session_semester_config_always
from .ug_serializer import (SettingSerializer,LecturerCourseSerializer,RegistrationStudSerializer,UndergraduateProgrammeSerializer,ClassBroadsheetSemesterSessionSerializer,
                    UndergraduateProgrammeSerializer,UndergraduateCourseSerializer)
from undergraduate.models import (Faculty, Department,Programme,Course,Curriculum,
Registration,RegSummary,LecturerCourse)


import json
from datetime import datetime


@login_required(login_url='index')
@api_view(['POST'])
def approve_disapprove_user_courses_in_semester(request):
    # # ug/api/approve-disapprove-user-courses-in-semester
    try:
        if 'email' in request.POST and request.POST['email'] and len(request.POST.getlist('courses[]'))>0:
            if request.data['type'].upper() == 'APPROVE':
                with transaction.atomic():
                    course_list = LecturerCourse.objects.select_for_update().filter(lecturer=request.data['email'],id__in=request.POST.getlist('courses[]'),settings=session_semester_config().id)
                    for course in course_list:
                        course.status = 'APPROVED'
                        course.save()
                    return Response({'status':'success','message':'Course(s) approved!','data':''}, status=status.HTTP_200_OK)
            elif request.data['type'].upper() == 'DISAPPROVE':
                with transaction.atomic():
                    course_list = LecturerCourse.objects.select_for_update().filter(lecturer=request.data['email'],id__in=request.POST.getlist('courses[]'),settings=session_semester_config().id)
                    for course in course_list:
                        course.status = 'PENDING'
                        course.save()
            else:
                return Response({'status':'failed','message':'Error with request type','data':''}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status':'failed','message':'Error with email/courses supplied','data':''}, status=status.HTTP_400_BAD_REQUEST)
    #     
    except LecturerCourse.DoesNotExist:
        return Response({'status':'failed','message':'Error performing action on lect courses','data':''}, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='index')
@api_view(['POST'])
def get_user_courses_in_semester_for_approval(request):
    # ug/api/get-user-courses-in-semester-for-approval
    if 'email' in request.POST.keys() and request.POST['email']:
        settings = session_semester_config()
        courses = [{'id':row.id,'course_code':row.course_code,'lecturer':row.lecturer.email}
         for row in LecturerCourse.objects.filter(lecturer=request.POST['email'],
        settings=settings.id, status='PENDING')]
        return Response({'status':'success','message':'Courses gotten successfully!','data':courses}, status=status.HTTP_200_OK)

    return Response({'status':'failed','message':'Error fetching courses','data':''}, status=status.HTTP_400_BAD_REQUEST)


