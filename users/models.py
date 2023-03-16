from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _




class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        user = self.model(email= self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('semester_session_id', Setting.objects.get(id=1))
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ICT1 = "ICT1", 'ICT1' # ICT
        ICT2 = "ICT2", 'ICT2' # ICT
        ICT3 = "ICT3", 'ICT3' # ICT
        FO = "FO", 'Faculty Officer' #Faculty Officer
        EO = "EO", 'Exam officer' #Exam officer
        LA = "LA", 'Level Adviser' # Level Adviser
        LEC = "LEC", 'Lecturer' # Lecturer
        HOD = "HOD", 'HOD' # HOD
        DEAN = "DEAN", 'DEAN' # Lecturer
    base_role = Role.LEC
    email = models.EmailField(_('email address'), unique=True)
    role = models.JSONField(default= dict,blank=True,null=True) 
    semester_session_id = models.ForeignKey('base.Setting',blank=False,null=False, on_delete=models.RESTRICT)
    programme = models.ForeignKey('undergraduate.Programme', related_name='programme_user_related', on_delete=models.RESTRICT,to_field='programme_id',blank=True,null=True)
    department = models.ForeignKey('undergraduate.Department', related_name='department_user_related', on_delete=models.RESTRICT,to_field='id',blank=True,null=True)
    faculty = models.ForeignKey('undergraduate.Faculty', related_name='faculty_user_related', on_delete=models.RESTRICT,to_field='id',blank=True,null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    ordering = ['-created']
    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
    
    
    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return False

    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return False

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin
    

    @property
    def user_roles_fo(self):
        if self.role.get(str(self.semester_session_id.id))  is not None:
            return self.Role.FO in self.role.get(str(self.semester_session_id.id)) #Faculty Officer
        return False
    @property
    def user_roles_eo(self):
        if self.role.get(str(self.semester_session_id.id))  is not None:
            return self.Role.EO in self.role.get(str(self.semester_session_id.id)) #Exam officer
        return False
    @property
    def user_roles_la(self):
        if self.role.get(str(self.semester_session_id.id))  is not None:
            return self.Role.LA in self.role.get(str(self.semester_session_id.id)) # Level Adviser
        return False
    @property
    def user_roles_lec(self):
        if self.role.get(str(self.semester_session_id.id))  is not None:
            return self.Role.LEC in self.role.get(str(self.semester_session_id.id)) # Lecturer
        return False
    @property
    def user_roles_hod(self):
        if self.role.get(str(self.semester_session_id.id))  is not None:
            return self.Role.HOD in self.role.get(str(self.semester_session_id.id)) # HOD
        return False
    @property
    def user_roles_dean(self):
        if self.role.get(str(self.semester_session_id.id))  is not None:
            return self.Role.DEAN in self.role.get(str(self.semester_session_id.id)) # DEAN
        return False
      
    


class LevelAdviser(models.Model):
    lecturer = models.ForeignKey('users.User', on_delete=models.RESTRICT)
    programme = models.ForeignKey('base.Programme', on_delete=models.RESTRICT)
    level = models.CharField(max_length=10)
    # last_updated_by = models.ForeignKey('users.User', on_delete=models.RESTRICT)
    settings = models.ForeignKey('base.Setting', on_delete=models.RESTRICT)
    approved_by = models.ForeignKey('users.User', related_name='users',blank=True,null=True, on_delete=models.RESTRICT)
    approved_at = models.DateTimeField(auto_now_add=True)
    approval_details = models.TextField(blank=True, null=True)
    # last_updated_by = models.CharField(max_length=50,null=True, blank=True)
    deleted = models.CharField(max_length=1, default='N',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "lecturer_level_adviser"

    def __str__(self) -> str:
        return f"{self.lecturer}_{self.programme}_{self.level}"




class LogUserRoleForSemester(models.Model):
    
    class Status(models.TextChoices):
        PENDING = "PENDING", 'PENDING' 
        APPROVED = "APPROVED", 'APPROVED'   
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_semester_role_related',to_field='email')
    roles = models.JSONField()
    semester_session = models.ForeignKey('base.Setting', on_delete=models.RESTRICT)
    programme = models.ForeignKey('undergraduate.Programme', related_name='programme_semester_role_related', on_delete=models.RESTRICT,to_field='programme_id')
    department = models.ForeignKey('undergraduate.Department', related_name='department_semester_role_related', on_delete=models.RESTRICT,to_field='id')
    approved_by = models.ForeignKey('users.User',to_field='email', related_name='approved_by_semester_role_related',on_delete=models.RESTRICT,null=True, blank=True)
    approved_at = models.DateTimeField(auto_now_add=True)
    role_status = models.CharField( max_length=15,choices=Status.choices, default= Status.PENDING)
    deleted = models.CharField(max_length=1, default='N',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "semester_user_roles_log"  #LogUserRoleForSemester
        unique_together = ('owner','semester_session')

    def __str__(self) -> str:
        return f"{self.owner}_{self.programme}_{self.department}"



