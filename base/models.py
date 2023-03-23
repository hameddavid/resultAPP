from django.db import models
from django.contrib import messages
from django.shortcuts import redirect
from users.models import User


class Staff(models.Model):
    user = models.OneToOneField(User,related_name='staff' ,on_delete=models.CASCADE,unique=True, blank=True, null=True,to_field='email')
    userid = models.CharField(max_length=255,null=True, blank=True, unique=True)
    email = models.CharField(max_length=255,null=True, blank=True, unique=True)
    phone = models.CharField(max_length=11,null=True, blank=True)
    password = models.TextField(max_length=255, null=True, blank=True)
    profile_image = models.TextField(max_length=255,null=True, blank=True)
    profile_image_small = models.TextField(max_length=255,null=True, blank=True)
    staff_type = models.CharField(max_length=10,null=True, blank=True)
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(max_length=255,null=True, blank=True)
    online = models.IntegerField(null=True, blank=True)
    activate = models.IntegerField(null=True, blank=True)
    pwdreset = models.IntegerField(null=True, blank=True)
    lastupdate = models.CharField(max_length=255,null=True, blank=True)
    form_completed =  models.IntegerField(null=True, blank=True)
    retired =  models.IntegerField(null=True, blank=True)
    adjunct =  models.IntegerField(null=True, blank=True)
    disengaged =  models.IntegerField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    r_date = models.CharField(max_length=255,null=True, blank=True)
    support_team =  models.IntegerField(null=True, blank=True)
    research_output =  models.IntegerField(null=True, blank=True)
    phd_output =  models.IntegerField(null=True, blank=True)
    msc_output =  models.IntegerField(null=True, blank=True)
    date = models.CharField(max_length=255,null=True, blank=True)

    title = models.CharField(max_length=50, null=True, blank=True)
    myprofile = models.TextField(null=True, blank=True)
    staff_no  = models.CharField(max_length=255, null=True, blank=True)
    sh_staff_no = models.CharField(max_length=255, null=True, blank=True)
    firstname = models.CharField(max_length=255, null=True, blank=True)
    middlename = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    former_firstname = models.CharField(max_length=255, null=True, blank=True)
    former_middlename = models.CharField(max_length=255, null=True, blank=True)
    former_lastname = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    mstatus = models.CharField(max_length=255, null=True, blank=True)
    dob = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True, blank=True)
    state_origin = models.CharField(max_length=255, null=True, blank=True)
    istate = models.CharField(max_length=255, null=True, blank=True)
    ipbirth = models.CharField(max_length=255, null=True, blank=True)
    date_app_uni = models.CharField(max_length=255, null=True, blank=True)
    date_app_pubservice = models.CharField(max_length=255, null=True, blank=True)
    p_address = models.TextField(null=True, blank=True)
    c_address = models.TextField(null=True, blank=True)
    r_address = models.TextField(null=True, blank=True)
    p_email = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True)
    landline = models.CharField(max_length=255, null=True, blank=True)
    office_phone = models.CharField(max_length=255, null=True, blank=True)
    intercom = models.CharField(max_length=255, null=True, blank=True)
    hobbies = models.TextField(null=True, blank=True)
    pob = models.CharField(max_length=255, null=True, blank=True)
    poblga = models.CharField(max_length=255, null=True, blank=True)
    health = models.CharField(max_length=255, null=True, blank=True)
    cv = models.CharField(max_length=255, null=True, blank=True)
    signature = models.CharField(max_length=255, null=True, blank=True)
    employment_type = models.CharField(max_length=255, null=True, blank=True)
    form_completed = models.CharField(max_length=255, null=True, blank=True)
    email_status = models.IntegerField(null=True, blank=True)
    covenant = models.IntegerField(null=True, blank=True)
    leave_app = models.IntegerField(null=True, blank=True)
    retired = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = "staff"

    def __str__(self) -> str:
        return f"{self.userid}--{self.email}"


# class StaffProfile(models.Model):
#     # staff = models.ForeignKey(Staff, to_field='userid' ,on_delete=models.CASCADE)
#     title = models.CharField(max_length=50, null=True, blank=True)
#     myprofile = models.TextField(null=True, blank=True)
#     staff_no  = models.CharField(max_length=255, null=True, blank=True)
#     sh_staff_no = models.CharField(max_length=255, null=True, blank=True)
#     firstname = models.CharField(max_length=255, null=True, blank=True)
#     middlename = models.CharField(max_length=255, null=True, blank=True)
#     lastname = models.CharField(max_length=255, null=True, blank=True)
#     former_firstname = models.CharField(max_length=255, null=True, blank=True)
#     former_middlename = models.CharField(max_length=255, null=True, blank=True)
#     former_lastname = models.CharField(max_length=255, null=True, blank=True)
#     gender = models.CharField(max_length=255, null=True, blank=True)
#     mstatus = models.CharField(max_length=255, null=True, blank=True)
#     dob = models.CharField(max_length=255, null=True, blank=True)
#     nationality = models.CharField(max_length=255, null=True, blank=True)
#     state_origin = models.CharField(max_length=255, null=True, blank=True)
#     istate = models.CharField(max_length=255, null=True, blank=True)
#     ipbirth = models.CharField(max_length=255, null=True, blank=True)
#     date_app_uni = models.CharField(max_length=255, null=True, blank=True)
#     date_app_pubservice = models.CharField(max_length=255, null=True, blank=True)
#     p_address = models.TextField(null=True, blank=True)
#     c_address = models.TextField(null=True, blank=True)
#     r_address = models.TextField(null=True, blank=True)
#     p_email = models.CharField(max_length=255, null=True, blank=True)
#     mobile = models.CharField(max_length=255, null=True, blank=True)
#     landline = models.CharField(max_length=255, null=True, blank=True)
#     office_phone = models.CharField(max_length=255, null=True, blank=True)
#     intercom = models.CharField(max_length=255, null=True, blank=True)
#     hobbies = models.TextField(null=True, blank=True)
#     pob = models.CharField(max_length=255, null=True, blank=True)
#     poblga = models.CharField(max_length=255, null=True, blank=True)
#     health = models.CharField(max_length=255, null=True, blank=True)
#     cv = models.CharField(max_length=255, null=True, blank=True)
#     signature = models.CharField(max_length=255, null=True, blank=True)
#     employment_type = models.CharField(max_length=255, null=True, blank=True)
#     form_completed = models.CharField(max_length=255, null=True, blank=True)
#     email_status = models.IntegerField(null=True, blank=True)
#     covenant = models.IntegerField(null=True, blank=True)
#     leave_app = models.IntegerField(null=True, blank=True)
#     retired = models.IntegerField(null=True, blank=True)
    
#     class Meta:
#         db_table = "profile"

#     def __str__(self) -> str:
#         return f"{self.staff_no}  {self.firstname}"


class Setting(models.Model):
    semester_name_choices = (
        ("FIRST SEMESTER", "FIRST SEMESTER"),
        ("SECOND SEMESTER", "SECOND SEMESTER")
    )
    semester_code_choices = (
        (1, 1),
        (2, 2)
    )
    status_choices = (
        ("NONE", "NONE"),
        ("ACTIVE", "ACTIVE")
    )
     
    session = models.CharField(max_length=9, null=False, blank=False)
    semester_name = models.CharField(choices=semester_name_choices, max_length=50, null=False, blank=False)
    semester_code = models.IntegerField(choices=semester_code_choices, null=False, blank=False)
    status = models.CharField(choices=status_choices ,max_length=15, default='NONE', null=True, blank=True)
    semester_open_close = models.BooleanField(default=False)  # True is open, false is close
    # last_updated_by = models.ForeignKey('users.User', on_delete=models.RESTRICT, default='Dev')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "settings"
        unique_together = ('session','semester_name','semester_code')

    def __str__(self) -> str:
        return f"{self.semester_name} {self.session}"
    
    def save(self, *args, **kwargs):
        if(len(self.session)<9):
            return redirect('registerPage')
        if self.status == "ACTIVE":
            Setting.objects.filter(status="ACTIVE").update(status="NONE",semester_open_close=False)
        super(Setting, self).save(*args, *kwargs)




class Faculty(models.Model):
    faculty = models.CharField(max_length=50, null=False, blank=False)
    # last_updated_by = models.ForeignKey('users.User', on_delete=models.RESTRICT)
    last_updated_by = models.CharField(max_length=50,null=True, blank=True)
    last_updated_by = models.CharField(max_length=50,null=True, blank=True)
    deleted = models.CharField(max_length=1, default='N',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "faculties"

    def __str__(self) -> str:
        return self.faculty
    
    def save(self, *args, **kwargs):
        self.faculty.upper()
        super(Faculty, self).save(*args, *kwargs)




class Department(models.Model):
    department = models.CharField(max_length=50, null=False, blank=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.RESTRICT)
    # last_updated_by = models.ForeignKey('users.User', on_delete=models.RESTRICT)
    last_updated_by = models.CharField(max_length=50,null=True, blank=True)
    deleted = models.CharField(max_length=1, default='N',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "departments"

    def __str__(self) -> str:
        return self.department



class Programme(models.Model):
    programme_id = models.CharField(max_length=10, primary_key=True)
    programme = models.CharField(max_length=50, null=False, blank=False)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    # last_updated_by = models.ForeignKey('users.User', on_delete=models.RESTRICT)
    last_updated_by = models.CharField(max_length=50,null=True, blank=True)
    deleted = models.CharField(max_length=1, default='N',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "programmes"

    def __str__(self) -> str:
        return self.programme




class Curriculum(models.Model):
    prog = models.ForeignKey(Programme, on_delete=models.CASCADE)
    course = models.ForeignKey('course.Course',on_delete=models.CASCADE)
    course_reg_level = models.CharField(max_length=45,null=True, blank=True)
    semester = models.CharField(max_length=1,null=True, blank=True)
    status =  models.CharField(max_length=10,null=True, blank=True)
    # last_updated_by_now = models.ForeignKey('users.User', on_delete=models.RESTRICT)
    # last_updated_by = models.CharField(max_length=50,null=True, blank=True)
    # last_update_date = models.CharField(max_length=1, default='N',null=True, blank=True)
    # register_flag = models.CharField(max_length=1, default='N',null=True, blank=True) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "curriculum"

    def __str__(self) -> str:
        return self.prog_code



# ########################### Study Signal, bulk-create ... 
class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    quantity = models.IntegerField()
    week = models.IntegerField()
    price = models.FloatField()

    class Meta:
         unique_together = ('name','quantity')


class Sale(models.Model):
    product = models.IntegerField()
    week = models.IntegerField()
    sales_amount = models.FloatField()
# ###########################    #####################################