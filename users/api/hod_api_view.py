from rest_framework.decorators import  api_view
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import permissions,authentication
from django.db.models import Prefetch



from users.models import User,LogUserRoleForSemester
from undergraduate.models import Programme, Department,Faculty,Student,Registration
from .serializers import (UserSerializer,UserRolesLoggerSerializer,
UserRolesLoggerSerializerHOD)
from base.baseHelper import session_semester_config, session_semester_config_always


@login_required(login_url='index')
@api_view(['POST'])
def approve_disapprove_user_roles_in_semester(request):
    # {"id":"2","type":"approve"}
    if 'id' in request.data and request.data['id'] and 'type' in request.data:
            try:
                roles_log = LogUserRoleForSemester.objects.filter(id=request.data.get('id')).first()
                if roles_log is not None:
                    user = User.objects.filter(email=roles_log.owner).first()
                else:
                    return Response({'status':'failed','message':'Error fetching user/roles 1','data':''}, status=status.HTTP_400_BAD_REQUEST)
            except LogUserRoleForSemester.DoesNotExist:
                return Response({'status':'failed','message':'Error fetching user/roles 2','data':''}, status=status.HTTP_400_BAD_REQUEST)

            if request.method == 'POST' and request.data.get('type').upper() == 'APPROVE':  
                roles_log.role_status = "APPROVED"
                roles_log.approved_by = request.user
                roles_log.save()
                user.role.update(roles_log.roles) 
                user.programme = Programme.objects.filter( programme_id=roles_log.programme_id).first()
                department = Department.objects.filter( id=roles_log.id).first() 
                user.department = department
                user.faculty = Faculty.objects.filter( id=department.faculty_id).first() 
                user.save()
                return Response({'status':'success','message':'User roles successfully approved'}, status=status.HTTP_200_OK)

            elif request.method == 'POST' and request.data.get('type').upper() == 'DISAPPROVE':
                roles_log.role_status = "PENDING"
                roles_log.approved_by = None
                roles_log.save()
                user.role[session_semester_config().id] = []
                user.programme = None
                user.department = None
                user.save()
                return Response({'status':'success','message':'User roles successfully disapproved'}, status=status.HTTP_200_OK)

            else :
                return Response({'status':'failed','message':'Error with request type and HTTP verb','data':''}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'status':'failed','message':'id and request type are required','data':''}, status=status.HTTP_400_BAD_REQUEST)
    
    