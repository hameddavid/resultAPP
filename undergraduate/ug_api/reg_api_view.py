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
    
    return Response({'status':'failed','message':'Cant find course code','data':''}, status=status.HTTP_400_BAD_REQUEST)

        
    
@login_required(login_url='index')
@api_view(['POST'])
def mass_submit_student_reg_score(request):
    try:
        csv_file = request.FILES['course_file']
        if  csv_file.name.endswith('.csv'):
            reader = pd.read_csv(csv_file)
            settings = session_semester_config()
            res_data = []
            with transaction.atomic():
                for  _, row in reader.iterrows():
                    updated = Registration.objects.filter(matric_number_fk=row[0],
                    course_code= request.POST['course_code'],session_id=settings.session,semester=settings.semester_code).update(score=row[1])
                    if updated !=1:
                        res_data.append(row[0])
            return Response({'status':'success','message':'Records updated successfully!','data':res_data}, status=status.HTTP_200_OK)

        return Response({'status':'failed','message':'Error updating rocord','data':''}, status=status.HTTP_400_BAD_REQUEST)

    except:

        return Response({'status':'failed','message':'Error updating rocord from catch','data':''}, status=status.HTTP_400_BAD_REQUEST)

    
#     from django.shortcuts import render
# from rest_framework import generics
# import io, csv, pandas as pd
# from rest_framework.response import Response
# # remember to import the File model
# # remember to import the FileUploadSerializer and SaveFileSerializer
# class UploadFileView(generics.CreateAPIView):
#     serializer_class = FileUploadSerializer
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         file = serializer.validated_data['file']
#         reader = pd.read_csv(file)
#         for _, row in reader.iterrows():
#             new_file = File(
#                        id = row['id'],
#                        staff_name= row["Staff Name"],
#                        position= row['Designated Position'],
#                        age= row["Age"],
#                        year_joined= row["Year Joined"]
#                        )
#             new_file.save()
#         return Response({"status": "success"},
#                         status.HTTP_201_CREATED)
    # if 'course_code' in request.POST and request.POST['course_code']:
    #     reg_score = [{'id':key, 'score':value} for key,value in request.POST.items() if key !='course_code']
    #     Registration.objects.bulk_update(
    #         [Registration(id= row['id'], score=row['score'])
    #         for row in reg_score],
    #         ["score"],
    #         batch_size=1000)
        # return Response({'status':'success','message':'Records updated successfully!','data':''}, status=status.HTTP_200_OK)
    
    return Response({'status':'failed','message':'Cant find course code','data':''}, status=status.HTTP_200_OK)

        
    