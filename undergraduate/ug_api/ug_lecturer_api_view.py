from rest_framework.views import APIView
from rest_framework.decorators import  api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions,authentication
from base.baseHelper import session_semester_config, session_semester_config_always
from .ug_serializer import (SettingSerializer,LecturerCourseSerializer)
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

