from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.utils.translation import gettext as _


class Faculty(models.Model):
    faculty = models.CharField(max_length=191, null=False, blank=False)
    last_updated_by_old = models.CharField(max_length=191, null=False, blank=False,default=' ')
    last_updated_by_new = models.ForeignKey('users.User',to_field='email', on_delete=models.RESTRICT, null=True, blank=False, related_name='ug_faculty_user_related')
    deleted = models.CharField(max_length=1, default='N',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ug_faculties"

    def __str__(self) -> str:
        return self.faculty
    
    def save(self, *args, **kwargs):
        self.faculty.upper()
        super(Faculty, self).save(*args, *kwargs)




class Department(models.Model):
    department = models.CharField(max_length=50, null=False, blank=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.RESTRICT)
    last_updated_by = models.ForeignKey('users.User',to_field='email', on_delete=models.RESTRICT, null=True, blank=True, related_name='ug_department_user_related')
    deleted = models.CharField(max_length=1, default='N',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ug_departments"

    def __str__(self) -> str:
        return self.department
        
    def save(self, *args, **kwargs):
        self.department.upper()
        super(Department, self).save(*args, *kwargs)


class Programme(models.Model):
    programme_code = models.CharField( max_length=10, unique=True )
    programme = models.CharField(max_length=50, )
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    required_ctcup = models.IntegerField(default=0,null=True, blank=True)   #REQUIRED_CTCUP
    required_cteup = models.IntegerField(default=0,null=True, blank=True)   #REQUIRED_CTEUP
    last_updated_by = models.ForeignKey('users.User',to_field='email', on_delete=models.RESTRICT,null=True, blank=True, related_name='ug_programme_user_related')
    deleted = models.CharField(max_length=1, default='N')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ug_programmes"

    def __str__(self) -> str:
         return "{} ({})".format(self.programme, self.programme_code)
    
    def save(self, *args, **kwargs):
        self.programme.upper()
        self.programme_code.upper()
        super(Programme, self).save(*args, *kwargs)




class CourseManager(models.Manager):
    def get_current_courses_instance(self):
        all_courses = Course.objects.all().order_by("-unit_id")
        all_current_instance = []
        all_duplicate_instance = set()
        for instance in all_courses:
            if instance.course_code not in  all_duplicate_instance:
                all_current_instance.append(instance)
                all_duplicate_instance.add(instance.course_code)
        return all_current_instance


class Course(models.Model):
    course_id	= models.CharField(max_length=50, primary_key=True)
    course_code	= models.CharField(max_length=45, null=False,blank=False)
    course_title = models.CharField(max_length=191,null=True,blank=True)
    unit	= models.IntegerField(null=True,blank=True)
    status = models.CharField(max_length=20,null=True,blank=True)
    course_id_of_equivalence = models.CharField(max_length=45, null=True,blank=True)
    last_updated_by_old	= models.CharField(max_length=45,null=True,blank=True)
    last_update_date = models.CharField(max_length=45,null=True,blank=True)
    course_level = models.CharField(max_length=10,null=True,blank=True)
    register_flag = models.CharField(max_length=10,null=True,blank=True)
    deleted = models.CharField(max_length=1,null=True,blank=True)
    unit_id	= models.CharField(max_length=45,null=True,blank=True)
    last_updated_by_new = models.ForeignKey('users.User',to_field='email', on_delete=models.RESTRICT,related_name='ug_course_user_related',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ug_courses"
        unique_together = ('course_code', 'unit_id') 

    def __str__(self) -> str:
        return self.course_id
    objects = CourseManager()

    def save(self, *args, **kwargs):
        self.course_id = f"{self.course_code}*{self.unit_id}"
        super(Course, self).save(*args, *kwargs)


class Curriculum(models.Model):
    class Status(models.TextChoices):
        ELECTTIVE = "E", 'ELECTTIVE' 
        COMPULSORY = "C", 'COMPULSORY' 
    class Deleted(models.TextChoices):
        YES = "Y", 'YES' 
        NO = "N", 'NO' 
    class RegisterFlag(models.TextChoices):
        YES = "Y", 'YES' 
        NO = "N", 'NO' 
    class Semester(models.TextChoices):
        FIRST_SEMESTER = "1", 'FIRST SEMESTER' 
        SECOND_SEMESTER = "2", 'SECOND_SEMESTER' 
    class CourseRegLevel(models.TextChoices):
        ONE_H = "100", '100' 
        TWO_H = "200", '200' 
        THREE_H = "300", '300' 
        FOUR_H = "400", '400' 
        FIVE_H = "500", '500' 
        SIX_H = "600", '600' 
        SEVEN_H = "700", '700' 
        
    programme = models.ForeignKey(Programme, on_delete=models.RESTRICT, related_name='ug_curriculum_program_related',to_field='programme_code')
    course_code = models.CharField(max_length=15, null=False, blank=False)
    status =  models.CharField(max_length=1, choices=Status.choices, default=Status.COMPULSORY)
    last_updated_by_old = models.CharField(max_length=191,null=True, blank=True,default=' ')
    last_updated_date_old = models.CharField(max_length=191,null=True, blank=True)
    course_reg_level = models.CharField(max_length=10, choices=CourseRegLevel.choices, default=CourseRegLevel.ONE_H)
    semester = models.CharField(max_length=1, choices=Semester.choices, default=Semester.FIRST_SEMESTER)
    register_flag = models.CharField(max_length=2, choices=RegisterFlag.choices, default=RegisterFlag.YES)
    deleted = models.CharField(max_length=1, choices=Deleted.choices, default=Deleted.NO)
    last_updated_by_new = models.ForeignKey('users.User',to_field='email', on_delete=models.RESTRICT, related_name='ug_curriculum_user_related',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ug_curriculum"
        unique_together = ('programme', 'course_code') 

    def save(self, *args, **kwargs):
        if 'request' in kwargs and self.last_updated_by_new is None:
            request = kwargs.pop('request')
            self.last_updated_by_new= request.user
        super(Curriculum, self).save(*args, *kwargs)

    def clean(self):
        check_course = Course.objects.filter(course_code = self.course_code).first()
        if check_course is None:
            raise ValidationError({'course_code': _('Course Code must be contained in the Course table!!')})


    def __str__(self) -> str:
        return f"{self.programme} {self.course_code} {self.course_reg_level}"



class Student(models.Model):
    matric_number = models.CharField(max_length=50, null=False,blank=False,unique=True)
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
    last_updated_by_old = models.CharField(max_length=50,null=True,blank=True, default=' ')
    last_update_date_old = models.CharField(max_length=50,null=True,blank=True)
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
    notify_sms = models.CharField(max_length=1,null=True,blank=True, default='N')
    notify_email = models.CharField(max_length=1,null=True,blank=True, default='N')
    parent_pwd = models.CharField(max_length=191,null=True,blank=True)
    registration_pwd = models.CharField(max_length=191,null=True,blank=True, default='password')
    financial_flag = models.CharField(max_length=1,null=True,blank=True, default='N')
    notify_bursary_sms = models.CharField(max_length=1,null=True,blank=True, default='N')	
    jamb_reg = models.CharField(max_length=50,null=True,blank=True)
    run_mail = models.CharField(max_length=100,null=True,blank=True)
    degree_sought = models.CharField(max_length=100,null=True,blank=True)
    acad_status = models.CharField(max_length=50,null=True,blank=True, default='GSD')
    entry_mode = models.CharField(max_length=50,null=True,blank=True, default='UME')
    hold_record = models.CharField(max_length=1,null=True,blank=True)
    run_mail_2 = models.CharField(max_length=191,null=True,blank=True)	
    gpa = models.FloatField(null=True,blank=True)
    last_updated_by_new = models.ForeignKey('users.User',to_field='email', on_delete=models.RESTRICT, related_name='ug_student_user_related',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ug_students"

    def __str__(self) -> str:
        return self.matric_number

class ErrorLog(models.Model):
    process_name = models.CharField(max_length=30, null=True, blank=True)
    message_date = models.CharField(max_length=30, null=True, blank=True)
    message_desc = models.TextField(null=True, blank=True)
    last_updated_by = models.ForeignKey('users.User',to_field='email', on_delete=models.RESTRICT, related_name='ug_errorlog_user_related',null=True,blank=True)
    last_updated_date = models.CharField(max_length=25,null=True, blank=True)
    deleted = models.CharField(max_length=1,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "ug_errorLog"

    def __str__(self) -> str:
        return self.process_name

class History1(models.Model):
    trans_id = models.IntegerField()
    matric_number = models.CharField(max_length=30,null=True, blank=True)
    course_code = models.CharField(max_length=30,null=True, blank=True)
    action_message = models.TextField(null=True, blank=True)
    last_updated_by = models.ForeignKey('users.User',to_field='email', on_delete=models.RESTRICT, related_name='ug_history1_user_related',null=True,blank=True)
    deleted = models.CharField(max_length=1,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ug_history1"

    def __str__(self) -> str:
        return self.trans_id


class Lecturer(models.Model):
    firstname = models.CharField(max_length=30,null=True,blank=True)
    surname = models.CharField(max_length=30,null=True,blank=True)
    Lecturer_id = models.CharField(max_length=30,null=True,blank=True)
    programme = models.CharField(max_length=30,null=True,blank=True)
    phone = models.CharField(max_length=30,null=True,blank=True)
    campus_text = models.CharField(max_length=30,null=True,blank=True)
    email = models.CharField(max_length=30,null=True,blank=True)
    last_updated_by = models.CharField(max_length=30,null=True,blank=True)
    last_updated_date = models.CharField(max_length=30,null=True,blank=True)
    deleted = models.CharField(max_length=1, default='N')
    login_name = models.CharField(max_length=30,null=True,blank=True)
    courses = models.TextField(null=True,blank=True)
    prog_code = models.TextField(null=True,blank=True)
    user_code = models.CharField(max_length=191,null=True,blank=True)
    title = models.CharField(max_length=30,null=True,blank=True)
    notify_sms = models.CharField(max_length=1,null=True,blank=True)
    
    class Meta:
        db_table = "ug_lecturer"

    def __str__(self) -> str:
        return f"{self.firstname}  {self.surname}"


class OutstandException(models.Model):
    # matric_number = models.ForeignKey(Student, on_delete=models.RESTRICT, related_name='ug_outExc_student_related',null=True,blank=True)
    # course_code = models.ForeignKey(Course, on_delete=models.RESTRICT, related_name='ug_outExc_student_related',null=True,blank=True)
    matric_number = models.CharField(max_length=30, null=True,blank=True)
    course_code = models.CharField(max_length=30, null=True,blank=True)
    last_updated_by = models.CharField(max_length=30, null=True,blank=True)
    last_updated_date = models.CharField(max_length=30, null=True,blank=True)
    deleted = models.CharField(max_length=1, null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ug_outstanding_exception"

    def __str__(self) -> str:
        return f"{self.matric_number}  {self.course_code}"

    
class RegSummary(models.Model):
    matric_number_fk = models.ForeignKey(Student,to_field='matric_number', related_name='ug_reg_sum_related', on_delete=models.RESTRICT,blank=True, null=True)
    semester = models.CharField(max_length=30, null=True, blank=True)
    session_id = models.CharField(max_length=30, null=True, blank=True)
    courses_taken = models.IntegerField( null=True, blank=True)
    courses_passed = models.IntegerField( null=True, blank=True)
    courses_failed = models.IntegerField( null=True, blank=True)
    tnur = models.IntegerField( null=True, blank=True)
    tnup = models.IntegerField( null=True, blank=True)
    tnuf = models.IntegerField( null=True, blank=True)
    wcrp = models.IntegerField( null=True, blank=True)
    gpa = models.DecimalField( max_digits=5, decimal_places=2)
    remarks = models.CharField(max_length=30, null=True, blank=True)
    last_updated_by_old = models.CharField(max_length=30, null=True, blank=True)
    last_updated_date_old = models.CharField(max_length=30, null=True, blank=True)
    deleted = models.CharField(max_length=1, null=True, blank=True)
    ctnur = models.DecimalField( max_digits=5, decimal_places=2,blank=True, null=True)
    ctnup = models.DecimalField( max_digits=5, decimal_places=2,blank=True, null=True)
    cgpa = models.DecimalField( max_digits=5, decimal_places=2,blank=True, null=True)
    ctcp = models.DecimalField( max_digits=5, decimal_places=2,blank=True, null=True)
    ctcup = models.DecimalField( max_digits=5, decimal_places=2,blank=True, null=True)
    cteup = models.DecimalField( max_digits=5, decimal_places=2,blank=True, null=True)
    acad_status = models.CharField(max_length=30,blank=True, null=True)
    last_updated_by_new = models.ForeignKey('users.User',to_field='email', on_delete=models.RESTRICT, related_name='ug_reg_summary_user_related',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ug_reg_summary"
        unique_together = ('matric_number_fk','semester','session_id') 

    def __str__(self) -> str:
        return f"{self.matric_number_fk}  {self.session_id} {self.semester}"




#  q = Student.objects.select_related('ug_reg_stud_related').filter(ug_reg_stud_related__session_id='2019/2020',ug_reg_stud_related__semester='1',prog_code='NUR')

class Registration(models.Model):
    DELETED_CHOICES = [('N','N'),('Y','Y')]
    matric_number_fk = models.ForeignKey(Student,to_field='matric_number', related_name='ug_reg_stud_related', on_delete=models.RESTRICT,blank=True, null=True)
    semester = models.CharField(max_length=30, blank=False, null=False)
    session_id = models.CharField(max_length=30, blank=False, null=False)
    course_code = models.CharField(max_length=30, blank=False, null=False)
    Lecturer_id = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=5, blank=False, null=False)
    unit = models.IntegerField(default=0)
    score = models.IntegerField(blank=False, null=False)
    grade = models.CharField(max_length=5, blank=True, null=True)
    remarks = models.CharField(max_length=45, blank=True, null=True)
    last_updated_date_old = models.CharField(max_length=30, null=True, blank=True)
    last_updated_by_old = models.CharField(max_length=30, null=True, blank=True)
    deleted = models.CharField(max_length=1,choices=DELETED_CHOICES, default='N')
    satisfied = models.CharField(max_length=5,blank=True, null=True)
    unit_id =  models.CharField(max_length=45, blank=False, null=False)
    app_user_id = models.CharField(max_length=191, blank=True, null=True)
    level = models.CharField(max_length=5,blank=True, null=True)
    record_status = models.CharField(max_length=5,blank=True, null=True, default='OFF') #ON/OFF
    last_updated_by_new = models.ForeignKey('users.User',to_field='email', on_delete=models.RESTRICT, related_name='ug_registration_user_related',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ug_registration"
        unique_together = ('matric_number_fk','semester','session_id','course_code') 

    def __str__(self) -> str:
        return f"{self.matric_number_fk}  {self.session_id} {self.semester}"



class RunregTransHistory(models.Model):
    trans_id = models.IntegerField()
    matric_number = models.CharField(max_length=100)
    course_code = models.CharField(max_length=30, blank=True, null=True)
    action_message = models.TextField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=30, blank=True, null=True)
    last_updated_date = models.CharField(max_length=30, blank=True, null=True)
    deleted = models.CharField(max_length=1, blank=True, null=True, default='N')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ug_Runreg_trans_history"

    def __str__(self) -> str:
        return f"{self.trans_id}  {self.matric_number} {self.course_code}"


class Session(models.Model):
    session_id = models.CharField(max_length=10)  
    semester = models.CharField(max_length=15)  
    session_desc = models.CharField(max_length=100)  
    start_date = models.CharField(max_length=30, blank=True, null=True)
    end_date = models.CharField(max_length=30, blank=True, null=True)
    last_updated_by = models.CharField(max_length=50, blank=True, null=True)
    last_updated_date = models.CharField(max_length=50, blank=True, null=True)
    deleted = models.CharField(max_length=1, blank=True, null=True, default='N')   
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



class LecturerCourse(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", 'PENDING' 
        APPROVED = "APPROVED", 'APPROVED' 
    course_code = models.CharField(max_length=45, null=False,blank=False)
    lecturer = models.ForeignKey('users.User', related_name='LecCourse_lecturer_rn', to_field='email', on_delete=models.RESTRICT, null=False,blank=False)
    status =  models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    settings = models.ForeignKey('base.Setting', related_name='LecCourse_settings_rn', on_delete=models.RESTRICT, null=False,blank=False)
    programme = models.ForeignKey('undergraduate.Programme', on_delete=models.RESTRICT,to_field='programme_code')
    department = models.ForeignKey('undergraduate.Department', on_delete=models.RESTRICT, to_field='id')
    approved_by = models.ForeignKey('users.User', related_name='LecCourse_approved_by_rn', to_field='email',blank=True,null=True, on_delete=models.RESTRICT)
    approved_at = models.DateTimeField(auto_now_add=True)
    approval_details = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ug_lecturers_courses"
        unique_together = ('course_code', 'lecturer','settings') 

    def __str__(self) -> str:
        return f"{self.course_code} - {self.lecturer}"



