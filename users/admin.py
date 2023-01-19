
from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import (User, LogUserRoleForSemester)
from base.baseHelper import session_semester_config

# admin.site.unregister(User)

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','role')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

   

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password',  'is_active', 'is_admin')


@admin.action(description='Deactivate selected users')
def deactivate_users(modeladmin, request, queryset):
    queryset.filter(is_superuser=False, is_admin=False).update(is_active=False)

@admin.action(description='Activate selected users')
def activate_users(modeladmin, request, queryset):
    queryset.filter(is_superuser=False, is_admin=False).update(is_active=True)

@admin.action(description='Deactivate all users in current semester')
def deactivate_users_in_semester(modeladmin, request, queryset):
    queryset.filter(is_superuser=False, is_admin=False,semester_session_id=session_semester_config().id).update(is_active=False)

@admin.action(description='Activate all users in current semester')
def activate_users_in_semester(modeladmin, request, queryset):
    queryset.filter(is_superuser=False, is_admin=False,semester_session_id=session_semester_config().id).update(is_active=True)

@admin.action(description='Add users to current semester')
def add_to_current_semester(modeladmin, request, queryset):
    queryset.filter(is_superuser=False, is_admin=False).update(semester_session_id=session_semester_config().id)

@admin.action(description='Remove users from current semester')
def remove_to_current_semester(modeladmin, request, queryset):
    queryset.filter(is_superuser=False, is_admin=False).update(semester_session_id=1)


@admin.register(User)
class MyUserAdmin(UserAdmin):
 # The forms to add and change user instances
    model = User
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email','programme','department','semester_session_id', 'role', 'is_admin','is_active','created')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('programme','department','role',)}),
        ('Permissions', {'fields': ('is_admin','is_active',)}),
        ('Important dates',{'fields':('last_login','created')}),
        ('Advanced options',{ 'classes':('collapse',),'fields':('groups','user_permissions') }),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_admin','is_active',),
        }),
    )
    search_fields = ('email','programme__programme','department__department',)
    ordering = ('email','-created',)
    filter_horizontal = ()
    readonly_fields = ['created',]
    list_editable = ['is_active','is_admin']
    list_per_page = 20
    # def get_actions(self, request):
    #     actions = super(ReadOnlyAdminMixin, self).get_actions(request)
    #     del actions["delete_selected"]
    #     return actions
    actions = [activate_users,deactivate_users,deactivate_users_in_semester,activate_users_in_semester,add_to_current_semester,remove_to_current_semester]
    # prepopulated_fields = {'slug': ['title']}


    def save_model(self, request, obj, form, change):
        obj.semester_session_id = session_semester_config()
        super().save_model(request, obj, form, change)


@admin.register(LogUserRoleForSemester)
class LogUserRoleForSemesterAdmin(admin.ModelAdmin):
    pass

