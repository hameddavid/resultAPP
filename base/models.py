from django.db import models
# from users.models import CustomUser


class Staff(models.Model):
    userid = models.CharField(max_length=200,null=False, blank=False, unique=True)
    email = models.CharField(max_length=200,null=False, blank=False, unique=True)
    phone = models.CharField(max_length=11,null=False, blank=False)
    password = models.TextField(null=False, blank=False)
    profile_image = models.TextField(null=False, blank=False)
    profile_image_small = models.TextField(null=False, blank=False)
    staff_type = models.CharField(max_length=10,null=False, blank=False)
    question = models.TextField(null=False, blank=False)
    answer = models.TextField(null=False, blank=False)
    online = models.IntegerField(null=False, blank=False)
    activate = models.IntegerField(null=False, blank=False)
    pwdreset = models.IntegerField(null=False, blank=False)
    lastupdate = models.CharField(max_length=255,null=False, blank=False)
    form_completed =  models.IntegerField(null=False, blank=False)
    retired =  models.IntegerField(null=False, blank=False)
    adjunct =  models.IntegerField(null=False, blank=False)
    disengaged =  models.IntegerField(null=False, blank=False)
    reason = models.TextField(null=False, blank=False)
    r_date = models.CharField(max_length=255,null=False, blank=False)
    support_team =  models.IntegerField(null=False, blank=False)
    research_output =  models.IntegerField(null=False, blank=False)
    phd_output =  models.IntegerField(null=False, blank=False)
    msc_output =  models.IntegerField(null=False, blank=False)
    date = models.CharField(max_length=255,null=False, blank=False)
    

    class Meta:
        db_table = "staff"

    def __str__(self) -> str:
        return self.email


class StaffProfile(models.Model):
    staff = models.ForeignKey(Staff, to_field='userid' ,on_delete=models.CASCADE)
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
        db_table = "profile"

    def __str__(self) -> str:
        return f"{self.staff_no}  {self.firstname}"


class Setting(models.Model):
    session = models.CharField(max_length=50, null=False, blank=False)
    semester_name = models.CharField(max_length=50, null=False, blank=False)
    semester_code = models.IntegerField(null=False, blank=False)
    status = models.CharField(max_length=15, default='NONE', null=True, blank=True)
    # last_updated_by = models.ForeignKey('users.CustomUser', on_delete=models.RESTRICT, default='Dev')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "settings"

    def __str__(self) -> str:
        return self.session



class Faculty(models.Model):
    faculty = models.CharField(max_length=50, null=False, blank=False)
    # last_updated_by = models.ForeignKey('users.CustomUser', on_delete=models.RESTRICT)
    last_updated_by = models.CharField(max_length=50,null=True, blank=True)
    last_updated_by = models.CharField(max_length=50,null=True, blank=True)
    deleted = models.CharField(max_length=1, default='N',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "faculties"

    def __str__(self) -> str:
        return self.college



class Department(models.Model):
    department = models.CharField(max_length=50, null=False, blank=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.RESTRICT)
    # last_updated_by = models.ForeignKey('users.CustomUser', on_delete=models.RESTRICT)
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
    # last_updated_by = models.ForeignKey('users.CustomUser', on_delete=models.RESTRICT)
    last_updated_by = models.CharField(max_length=50,null=True, blank=True)
    deleted = models.CharField(max_length=1, default='N',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "programmes"

    def __str__(self) -> str:
        return self.programme_id




class Curriculum(models.Model):
    prog = models.ForeignKey(Programme, on_delete=models.CASCADE)
    course = models.ForeignKey('course.Course',on_delete=models.CASCADE)
    course_reg_level = models.CharField(max_length=45,null=True, blank=True)
    semester = models.CharField(max_length=1,null=True, blank=True)
    status =  models.CharField(max_length=10,null=True, blank=True)
    # last_updated_by_now = models.ForeignKey('users.CustomUser', on_delete=models.RESTRICT)
    # last_updated_by = models.CharField(max_length=50,null=True, blank=True)
    # last_update_date = models.CharField(max_length=1, default='N',null=True, blank=True)
    # register_flag = models.CharField(max_length=1, default='N',null=True, blank=True) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "curriculum"

    def __str__(self) -> str:
        return self.prog_code



