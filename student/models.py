from django.db import models

# Create your models here.

class Student(models.Model):
    matric_number = models.CharField(max_length=50,null=False,blank=False,unique=True)
    surname = models.CharField(max_length=50,null=True,blank=True)
    firstname = models.CharField(max_length=50,null=True,blank=True)
    sex = models.CharField(max_length=1,null=True,blank=True)
    birth_date = models.CharField(max_length=50,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    lga = models.CharField(max_length=191,null=True,blank=True)	
    current_level = models.CharField(max_length=5,null=True,blank=True)
    state_origin = models.CharField(max_length=50,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    programme = models.CharField(max_length=191,null=True,blank=True)
    city_resident = models.CharField(max_length=100,null=True,blank=True)
    state_resident = models.CharField(max_length=100,null=True,blank=True)
    matric_date = models.CharField(max_length=50,null=True,blank=True)
    graduation_date = models.CharField(max_length=50,null=True,blank=True)
    status = models.CharField(max_length=50,null=True,blank=True)
    last_updated_by = models.CharField(max_length=50,null=True,blank=True)
    last_update_date = models.CharField(max_length=50,null=True,blank=True)
    deleted = models.CharField(max_length=1, default='N',null=True, blank=True)
    ctcp = models.IntegerField(null=True,blank=True)
    ctnur = models.IntegerField(null=True,blank=True)
    ctnup = models.IntegerField(null=True,blank=True)
    ctnuf = models.IntegerField(null=True,blank=True)
    cgpa = models.FloatField(null=True,blank=True)
    email1 = models.CharField(max_length=100,null=True,blank=True)
    email2 = models.CharField(max_length=100,null=True,blank=True)	
    student_phone = models.CharField(max_length=50,null=True,blank=True)
    parent_phone = models.CharField(max_length=50,null=True,blank=True)
    prog_code = models.CharField(max_length=50,null=True,blank=True)
    picture = models.CharField(max_length=191,null=True,blank=True)
    ctcup = models.IntegerField(null=True,blank=True)	
    cteup = models.IntegerField(null=True,blank=True)
    notify_sms = models.CharField(max_length=1,null=True,blank=True)
    notify_email = models.CharField(max_length=1,null=True,blank=True)
    parent_pwd = models.CharField(max_length=191,null=True,blank=True)
    registration_pwd = models.CharField(max_length=191,null=True,blank=True)
    financial_flag = models.CharField(max_length=1,null=True,blank=True)
    notify_bursary_sms = models.CharField(max_length=1,null=True,blank=True)	
    jamb_reg = models.CharField(max_length=50,null=True,blank=True)
    run_mail = models.CharField(max_length=100,null=True,blank=True)
    degree_sought = models.CharField(max_length=100,null=True,blank=True)
    acad_status = models.CharField(max_length=50,null=True,blank=True)
    entry_mode = models.CharField(max_length=50,null=True,blank=True)
    hold_record = models.CharField(max_length=1,null=True,blank=True)
    run_mail_2 = models.CharField(max_length=191,null=True,blank=True)	
    gpa = models.FloatField(null=True,blank=True)
    # last_updated_by_now = models.ForeignKey('users.User', on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "students"

    def __str__(self) -> str:
        return self.matric_number

