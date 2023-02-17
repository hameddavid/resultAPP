from rest_framework.decorators import  api_view
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import permissions,authentication
from django.db.models import Prefetch



from users.models import User,LogUserRoleForSemester
from undergraduate.models import Programme, Department,Student,Registration,Course,Curriculum
from .serializers import (UserSerializer,UserRolesLoggerSerializer,UserRolesLoggerSerializerHOD,)
from base.baseHelper import session_semester_config, session_semester_config_always



@api_view(['GET', 'POST'])
def user(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'message':'success','data':serializer.data}, status=status.HTTP_200_OK)




@login_required(login_url='index')
@api_view(['GET', 'POST','PUT','PATCH'])
def check_user_role_for_semester(request):
    if request.method == 'GET':
        owner = LogUserRoleForSemester.objects.filter(owner=request.user, semester_session=session_semester_config()).first()
        if owner is None:
            return Response({'status':'failed','message':'Kindly update your record for this semester','data':''}, status=status.HTTP_204_NO_CONTENT)
        elif owner is not None and owner.role_status == 'PENDING':
            # send email reminder to HOD
            return Response({'status':'failed','message':'Kindly remind your principal for necessary approval','data':''}, status=status.HTTP_204_NO_CONTENT)  
        elif owner is not None and owner.role_status == 'APPROVED':
            serializer = UserRolesLoggerSerializer(owner)
            return Response({'status':'success','message':'Kindly remind your principal for necessary approval','data':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response( {'status':'failed','message':'Unkown status','data':''}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        if request.data['department']:
            dpt= Department.objects.filter(id=request.data['department']).first().id  
            prog= Programme.objects.filter(department = dpt).first().programme_id
        elif request.data['programme']:
             prog= request.data.get('programme').split('*')[0] 
             dpt= Department.objects.filter(id=request.data.get('programme').split('*')[1]).first().id   
        serializer = UserRolesLoggerSerializer(data = {  
        "roles" : {session_semester_config().id: request.data.getlist('roles[]') or None},
        "programme": prog,
        "department": dpt,
        "semester_session": session_semester_config().id or None,
        "owner": request.user or None
         })
        if serializer.is_valid():
            serializer.save()
            # send email notification to the HOD
            return Response({'status':'success','message':'roles created!','data':''}, status=status.HTTP_200_OK)
        return Response(serializer.errors)
        return Response()
    if request.method == 'PUT':
        obj = LogUserRoleForSemester.objects.filter(owner=request.user, semester_session=session_semester_config()).first()
        serializer = UserRolesLoggerSerializer(obj, data={  
        "roles" : {session_semester_config().id: request.data.getlist('roles[]') or None},
        "programme": request.data.get('programme').split('*')[0]  or None,
        "department": Department.objects.filter(department=request.data.get('programme').split('*')[1]).first().id  or None,
        "semester_session": session_semester_config().id or None,
        "owner": request.user.id or None
         })    
        if serializer.is_valid():
            serializer.save()
             # send email notification to the HOD
            return Response({'status':'success','message':'roles updated!','data':serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors)
        # if owner is None:
        #     return Response({'status':'failed','message':'Are you accessing previous semester?','data':''}, status=status.HTTP_204_NO_CONTENT)
        # elif owner is not None and owner.role_status == 'PENDING':
        #     # send email reminder to HOD
        #     return Response({'status':'failed','message':'Kindly remind your principal for necessary approval','data':''}, status=status.HTTP_204_NO_CONTENT)  
        # elif owner is not None and owner.role_status == 'APPROVED':
        #     serializer = UserRolesLoggerSerializer(owner)
        #     return Response({'status':'failed','message':'Kindly remind your principal for necessary approval','data':serializer.data}, status=status.HTTP_200_OK)
        # else:
        #     return Response( {'status':'failed','message':'Unkown status','data':''}, status=status.HTTP_400_BAD_REQUEST)

    
    return Response( {'status':'failed','message':'Unkown status','data':''}, status=status.HTTP_400_BAD_REQUEST)


#          {
#     "roles": "[]",
#     "programme": "ACC",
#     "department":"15"
#  }
       



class TodoDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return LogUserRoleForSemester.objects.get(id=todo_id, user = user_id)
        except LogUserRoleForSemester.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, todo_id, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, todo_id, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = UserSerializer(instance = todo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, todo_id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )



class TodoListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = LogUserRoleForSemester.objects.filter(user = request.user.id)
        serializer = UserSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        # setting = Setting.objects.filter(user = request.user.id)
        # setting = Setting.objects.filter(status='ACTIVE').first()
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckUserRoleForSemester(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    queryset = LogUserRoleForSemester.objects.all()
    serializer_class = UserRolesLoggerSerializer

check_user_role_in_semester = CheckUserRoleForSemester.as_view()


class CheckUserRoleForSemesterHOD(generics.ListAPIView):
    queryset = LogUserRoleForSemester.objects.all()
    serializer_class = UserRolesLoggerSerializerHOD

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return LogUserRoleForSemester.objects.all().select_related('owner','programme')
        return LogUserRoleForSemester.objects.filter(department=user.department).select_related('owner','programme')
   
    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserRolesLoggerSerializerHOD(queryset, many=True)
        return Response(serializer.data)

check_user_role_in_semester_hod = CheckUserRoleForSemesterHOD.as_view()












