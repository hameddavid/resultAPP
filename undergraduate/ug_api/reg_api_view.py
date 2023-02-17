from rest_framework.views import APIView
from rest_framework.decorators import  api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions,authentication
from rest_framework import status, generics
from django.db.models import Prefetch
from django.db.models import Q
from base.baseHelper import session_semester_config, session_semester_config_always
from .ug_serializer import (SettingSerializer,LecturerCourseSerializer,RegistrationStudSerializer,UndergraduateProgrammeSerializer,ClassBroadsheetSemesterSessionSerializer,
                    UndergraduateProgrammeSerializer,UndergraduateCourseSerializer)
from undergraduate.models import (Faculty, Department,Programme,Student,Course,Curriculum,
Registration,RegSummary,LecturerCourse)








@login_required(login_url='index')
@api_view(['GET', 'POST'])
def submit_student_reg_score(request):
    if 'course_code' in request.POST and request.POST['course_code']:
        regs = Registration.objects.filter( Q(course_code=request.POST.get('course_code')) &
         Q(semester=session_semester_config().semester_code) & Q(session_id=session_semester_config().session)).values('matric_number_fk')
        # for row in regs:
        #     print(request.POST[row['matric_number_fk']], end='\n')
        
        for item in request.POST:
            print(item, end='\n')

        return Response({'status':'success','message':'Course code found','data':request.POST['course_code']}, status=status.HTTP_200_OK)
    
    return Response({'status':'failed','message':'Cant find course code','data':''}, status=status.HTTP_200_OK)

        
    