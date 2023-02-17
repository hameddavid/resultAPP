from rest_framework.views import APIView
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
from undergraduate.models import (Faculty, Department,Programme,Student,Course,Curriculum,
Registration,RegSummary,LecturerCourse)




import json
from datetime import datetime


class LecturerCourseView(APIView):

    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = LecturerCourseSerializer

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        queryset =  LecturerCourse.objects.all()
        serializer = LecturerCourseSerializer(queryset, many=True)
        return Response({"data":serializer.data})

    def post(self, request, format=None):
        data_filter = {
            'course_code': request.data.get('course_code').upper(),
            'lecturer':request.user.email,
            'settings':session_semester_config().id
        }
        serializer = LecturerCourseSerializer(data=data_filter)
        if serializer.is_valid():
            serializer.save()
            # send email notification to the HOD
            return Response({'status':'success','message':'Course added successfully!','data':''}, status=status.HTTP_200_OK)

        return Response(serializer.errors)


    def put(self, request, format=None):
       
        return Response({"data":"put data"})


lecturer_course_view = LecturerCourseView.as_view()



class ClassBroadsheetSemesterSessionList(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = ClassBroadsheetSemesterSessionSerializer

    def get_queryset(self):
        print(self.kwargs)
        user = self.request.user
        reg_q = Registration.objects.filter(session_id='2019/2020', semester='1')
        return Student.objects.prefetch_related(Prefetch('ug_reg_stud_related',queryset=reg_q)).filter(prog_code='NUR',current_level='400',
        status='CURRENT').order_by('matric_number')
   
    def list(self, request):
        queryset = self.get_queryset()
        serializer = ClassBroadsheetSemesterSessionSerializer(queryset, many=True)
        return Response(serializer.data)

class_broadsheet_semester_session_list = ClassBroadsheetSemesterSessionList.as_view()


class UndergraduateProgrammeList(generics.ListAPIView):
    queryset = Programme.objects.all()
    serializer_class = UndergraduateProgrammeSerializer

    def get_queryset(self):
        return Programme.objects.all().order_by('programme_id')
   
    def list(self, request):
        queryset = self.get_queryset()
        serializer = UndergraduateProgrammeSerializer(queryset, many=True)
        return Response(serializer.data)

undergraduate_programme_list = UndergraduateProgrammeList.as_view()



class UndergraduateCourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = UndergraduateCourseSerializer

    def get_queryset(self):
        return Course.objects.all().order_by('course_code')
   
    def list(self,request):
        queryset = self.get_queryset()
        serializer = UndergraduateCourseSerializer(queryset, many=True)
        return Response(serializer.data)

undergraduate_course_list = UndergraduateCourseList.as_view()



class UndergraduateCourseListCurriculumBased(generics.ListCreateAPIView,generics.UpdateAPIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = UndergraduateCourseSerializer

    def get_queryset(self):
        return Course.objects.filter(course_code__in=[row.course_code for row in
         Curriculum.objects.filter(programme = '')]).order_by('course_code')
   
    def list(self, request):
        queryset =  Course.objects.filter(course_code__in=[row.course_code for row in
         Curriculum.objects.filter(programme = request.user.programme)]).order_by('-unit_id')
        unique_courses = []
        track_courses = [] 
        for record in queryset:
            if record.course_code not in track_courses:
                track_courses.append(record.course_code)
                unique_courses.append(record)
        serializer = UndergraduateCourseSerializer(unique_courses, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # course_code lecturer status settings approved_by approved_at approval_details created updated
        if request.data.getlist('courses[]') and len(request.data.getlist('courses[]')) >0:
            courses_obj = [LecturerCourse(course_code=course, lecturer=request.user,
            status='PENDING', settings=session_semester_config(),programme=request.user.programme,department=request.user.department)
             for course in request.data.getlist('courses[]')]
            bulk_create = LecturerCourse.objects.bulk_create(courses_obj, ignore_conflicts=True)
            return Response({'status':'success','message':'Courses added successfully!','data':""}, status=status.HTTP_200_OK)

undergraduate_course_list_curriculum_base = UndergraduateCourseListCurriculumBased.as_view()




