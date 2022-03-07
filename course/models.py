from django.db import models

class Course(models.Model):
    course_id	= models.CharField(max_length=50, primary_key=True)
    course_code	= models.CharField(max_length=45, null=False,blank=False)
    course_description = models.CharField(max_length=191,null=True,blank=True)
    course_id_of_equivalence = models.CharField(max_length=45, null=True,blank=True)
    status = models.CharField(max_length=20,null=True,blank=True)
    unit	= models.IntegerField(null=True,blank=True)
    last_updated_by	= models.CharField(max_length=45,null=True,blank=True)
    last_update_date = models.CharField(max_length=45,null=True,blank=True)
    course_level = models.CharField(max_length=10,null=True,blank=True)
    register_flag = models.CharField(max_length=10,null=True,blank=True)
    deleted = models.CharField(max_length=1,null=True,blank=True)
    unit_id	= models.CharField(max_length=45,null=True,blank=True)
        # last_updated_by_now = models.ForeignKey('users.CustomUser', on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "courses"

    def __str__(self) -> str:
        return self.course_id



class LecturerCourse(models.Model):
    course = models.ForeignKey(Course, to_field='course_id', related_name='courses',on_delete=models.RESTRICT)
    lecturer = models.ForeignKey('users.CustomUser', to_field='email', on_delete=models.RESTRICT)
    status = models.PositiveIntegerField(default=0)
    settings = models.ForeignKey('base.Setting', on_delete=models.RESTRICT)
    time_approved = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lecturers_courses"
        unique_together = ('course', 'lecturer','settings') 

    def __str__(self) -> str:
        return self.course




# from django.db.models import UniqueConstraint
# from django.db.models.functions import Lower


# class MyModel(models.Model):
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)

#     class Meta:
#         constraints = [
#             UniqueConstraint(
#                 Lower('first_name'),
#                 Lower('last_name').desc(),
#                 name='first_last_name_unique',
#             ),
#         ]