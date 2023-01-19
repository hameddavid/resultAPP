from asyncio.windows_events import NULL
from django.db import models

# Create your models here.

class Course(models.Model):
    matric_number	= models.CharField(max_length=50, null=False,blank=False)
    semester	= models.CharField(max_length=1, null=False,blank=False)
    session = models.CharField(max_length=9,null=False,blank=False)
    course_code = models.CharField(max_length=7, null=False,blank=False)
    lecturer_id = models.CharField(max_length=20,null=True,blank=True, default=NULL)
    status	= models.CharField(max_length=1,null=False,blank=False, default='C')
    score	= models.CharField(max_length=2,null=False,blank=False, default=-1)
    grade = models.CharField(max_length=1,null=True,blank=True, default=NULL)
    remarks = models.CharField(max_length=60,null=True,blank=True, default=NULL)
    last_updated_date = models.CharField(max_length=191,null=True,blank=True)
    last_updated_by = models.CharField(max_length=191,null=True,blank=True)
    deleted = models.CharField(max_length=1,null=True,blank=True, default='N')
    satisfied = models.CharField(max_length=1,null=True,blank=True, default=NULL)
    unit_id	= models.CharField(max_length=8,null=False,blank=False, default=NULL)
        # last_updated_by_now = models.ForeignKey('users.User', on_delete=models.RESTRICT)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "registration"
        unique_together = ('matric_number', 'semester','session','course_code') 

    def __str__(self) -> str:
        return self.matric_number



class RegHistory(models.Model):
    matric_number	= models.CharField(max_length=50, null=False,blank=False, default=NULL)
    course_code = models.CharField(max_length=7, null=False,blank=False, default=NULL)
    action_message = models.TextField(null=True,blank=True, default=NULL)
    last_updated_by = models.CharField(max_length=191,null=True,blank=True, default=NULL)
    deleted = models.CharField(max_length=1,null=True,blank=True, default='N')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "RegHistory"
    

    def __str__(self) -> str:
        return self.matric_number




