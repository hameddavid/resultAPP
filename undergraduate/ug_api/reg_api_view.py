from rest_framework.views import APIView
from rest_framework.decorators import  api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions,authentication
from rest_framework import status, generics
from django.db.models import Prefetch
from django.db.models import Q
import io, csv, pandas as pd
from django.db import  transaction
from base.baseHelper import session_semester_config, session_semester_config_always
from .ug_serializer import (SettingSerializer,LecturerCourseSerializer,RegistrationStudSerializer,UndergraduateProgrammeSerializer,ClassBroadsheetSemesterSessionSerializer,
                    UndergraduateProgrammeSerializer,UndergraduateCourseSerializer)
from undergraduate.models import (Faculty, Department,Programme,Student,Course,Curriculum,
Registration,RegSummary,LecturerCourse)




@login_required(login_url='index')
@api_view(['GET', 'POST'])
def submit_student_reg_score(request):
    
    if 'course_code' in request.POST and request.POST['course_code']:
        reg_score = [{'id':key, 'score':value} for key,value in request.POST.items() if key !='course_code' and key !='myProjectTable_length' ]
        updated = Registration.objects.bulk_update(
            [Registration(id= row['id'], score=row['score'])
            for row in reg_score],
            ["score"],
            batch_size=1000)
        return Response({'status':'success','message':'Records updated successfully!','data':updated}, status=status.HTTP_200_OK)
    
    return Response({'status':'failed','message':'Cant find course code','data':''}, status=status.HTTP_200_OK)

        
    
@login_required(login_url='index')
@api_view(['POST'])
def mass_submit_student_reg_score(request):
    
    # if 'course_code' in request.POST and request.POST['course_code']:
    #     reg_score = [{'id':key, 'score':value} for key,value in request.POST.items() if key !='course_code']
    #     Registration.objects.bulk_update(
    #         [Registration(id= row['id'], score=row['score'])
    #         for row in reg_score],
    #         ["score"],
    #         batch_size=1000)
        # return Response({'status':'success','message':'Records updated successfully!','data':''}, status=status.HTTP_200_OK)
    
    return Response({'status':'failed','message':'Cant find course code','data':''}, status=status.HTTP_200_OK)

        
    