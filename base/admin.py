from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from base.baseHelper import session_semester_config

from .models import Staff,Setting  


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('session','semester_name','status','semester_open_close','created')
    list_filter = ('semester_open_close',)

@admin.register(Staff)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('title','firstname','lastname','staff_no','email','userid','phone',)
    list_filter = ('email',)


