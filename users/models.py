from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from base.models import Staff



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))

        user = self.model(email= self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    staff_no  = models.CharField(max_length=255, null=False, blank=False)
    sh_staff_no = models.CharField(max_length=255, null=False, blank=False)
    firstname = models.CharField(max_length=255, null=False, blank=False)
    middlename = models.CharField(max_length=255, null=False, blank=False)
    lastname = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=11,null=False, blank=False)
    profile_image = models.TextField(null=False, blank=False)
    profile_image_small = models.TextField(null=False, blank=False)
    signature = models.CharField(max_length=255, null=False, blank=False)
    retired =  models.IntegerField(null=False, blank=False)
    adjunct =  models.IntegerField(null=False, blank=False)
    disengaged =  models.IntegerField(null=False, blank=False)
    staff = models.ForeignKey('base.Staff', to_field='userid' ,on_delete=models.CASCADE)
    my_approved_courses = models.JSONField(default= dict) 
    role = models.JSONField(default= dict) 
    progId = models.JSONField(default= dict) 
    level = models.JSONField(default= dict) 
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    ordering = ['-created']
    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
    
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin




