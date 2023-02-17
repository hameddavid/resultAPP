from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from undergraduate.models import Programme, Department, Student, Registration,Course
from base.models import Setting

from users.models import User, LogUserRoleForSemester


class UserRolesLoggerSerializerHOD2(serializers.ModelSerializer):
    class Meta:
        model = LogUserRoleForSemester
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    owner_semester_role_related = UserRolesLoggerSerializerHOD2(read_only = True, many=True)
    class Meta:
        model = User
        fields = "__all__"


class UserRolesLoggerSerializer(serializers.ModelSerializer):
    semester_session= serializers.PrimaryKeyRelatedField(queryset=Setting.objects.all(),many=False, read_only=False)
    programme= serializers.PrimaryKeyRelatedField(queryset=Programme.objects.all(),many=False, read_only=False)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(),many=False, read_only=False)
    class Meta:
        model= LogUserRoleForSemester
        fields = ('roles','programme','department','semester_session', 'owner')
        
    def create(self, validated_data):
        #    
        return LogUserRoleForSemester.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # 
        instance.roles = validated_data.get('roles',instance.roles)
        instance.programme = validated_data.get('programme',instance.programme)
        instance.department = validated_data.get('department',instance.department)
        instance.save()
        return instance
#     {
#     "roles": "[]",
#     "programme": "ACC",
#     "department":"15",
#     "semester_session": "1",
#     "owner": "1"
# }


class UserRolesLoggerSerializerHOD(serializers.ModelSerializer):
    owner_semester_role_related = UserSerializer(read_only = True, many=True)
    class Meta:
        model = LogUserRoleForSemester
        fields = '__all__'


