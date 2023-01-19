from rest_framework import serializers
from undergraduate.models import LecturerCourse, Course
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

    