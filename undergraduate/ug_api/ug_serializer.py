from rest_framework import serializers
from undergraduate.models import (LecturerCourse,Course,Registration,Student,Programme)
from base.models import Setting


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['session','semester_name','semester_code','status']
       


class LecturerCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerCourse
        fields = ['course_code','lecturer','settings']
        # read_only_fields = ['lecturer']
    
    def validate(self, data):
        if len(data['course_code']) != 7 or Course.objects.filter(course_code=data['course_code']).first() == None :
            raise serializers.ValidationError('Invalid course code supplied!')
        return data
    def create(self, validated_data):
       
        return LecturerCourse.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass
        # 
        # instance.roles = validated_data.get('roles',instance.roles)
        # instance.programme = validated_data.get('programme',instance.programme)
        # instance.department = validated_data.get('department',instance.department)
        # instance.save()
        # return instance




class RegistrationStudSerializer(serializers.ModelSerializer):


    class Meta:
        model = Registration
        fields = ['course_code','status','score','unit','session_id','semester']


class ClassBroadsheetSemesterSessionSerializer(serializers.ModelSerializer):
    ug_reg_stud_related = RegistrationStudSerializer(many = True, read_only=True)


    class Meta:
        model = Student
        fields = ['matric_number','surname','firstname','ug_reg_stud_related']


class UndergraduateProgrammeSerializer(serializers.ModelSerializer):
    # ug_reg_stud_related = RegistrationStudSerializer(many = True, read_only=True)

    class Meta:
        model = Programme
        fields = "__all__"

class UndergraduateCourseSerializer(serializers.ModelSerializer):
    # ug_reg_stud_related = RegistrationStudSerializer(many = True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
