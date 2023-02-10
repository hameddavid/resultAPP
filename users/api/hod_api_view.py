from rest_framework.decorators import  api_view
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import permissions,authentication
from django.db.models import Prefetch



from users.models import User,LogUserRoleForSemester
from undergraduate.models import Programme, Department,Student,Registration
from .serializers import (UserSerializer,UserRolesLoggerSerializer,
UserRolesLoggerSerializerHOD,ClassBroadsheetSemesterSessionSerializer,UndergraduateProgrammeSerializer)
from base.baseHelper import session_semester_config, session_semester_config_always


@login_required(login_url='index')
@api_view(['POST'])
def approve_disapprove_user_roles_in_semester(request):
    print(request.data.get('id'))
    if request.data.get('id') is None:
        return Response({'status':'failed','message':'id and request type are required','data':''}, status=status.HTTP_400_BAD_REQUEST)
    try:
        roles_log = LogUserRoleForSemester.objects.filter(id=request.data.get('id'),role_status='PENDING').first()
        if roles_log is not None:
            user = User.objects.filter(email=roles_log.owner).first()
        else:
            return Response({'status':'failed','message':'Error fetching user/roles','data':''}, status=status.HTTP_400_BAD_REQUEST)
    except LogUserRoleForSemester.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST' and request.data.get('type').upper() == 'APPROVE':
        roles_log.role_status = "APPROVED"
        roles_log.approved_by = request.user
        roles_log.save()
        user.role = roles_log.roles
        user.programme = roles_log.programme
        user.department = roles_log.department
        user.save()
        # users = User.objects.all()
        # serializer = UserSerializer(users, many=True)
        # return Response({'message':'success','data':serializer.data}, status=status.HTTP_200_OK)
        return Response({'message':'success','data':''}, status=status.HTTP_200_OK)

    elif request.method == 'POST' and request.data.get('type').upper() == 'DISAPPROVE':
        return Response({'status':'success','message':'Success','data':''}, status=status.HTTP_200_OK)
        # users = User.objects.all()
        # serializer = UserSerializer(users, many=True)
        # return Response({'message':'success','data':serializer.data}, status=status.HTTP_200_OK)
    else :
        return Response({'status':'failed','message':'Error with request type and HTTP verb','data':''}, status=status.HTTP_400_BAD_REQUEST)