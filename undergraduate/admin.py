from django.contrib import admin
from .models import (Programme,Faculty,Department,Course,Curriculum,Student,
                    ErrorLog,History1,Lecturer,OutstandException,RegSummary,Registration,
                    RunregTransHistory,Session,)

# Register your models here.




@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ['course_code','course_title','unit','unit_id',]
    list_display = ['course_code','course_title','unit','status','unit_id','last_updated_by_new']
    list_editable = ['course_title','unit']
    ordering = ['course_code']
    search_fields = ('course_code','course_title')
    def save_model(self, request, obj, form, change):
        obj.last_updated_by_new = request.user
        super().save_model(request, obj, form, change)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    fields = ['faculty','deleted']
    list_display = ['id','faculty','deleted','last_updated_by_new','created']
    list_editable = ['faculty','deleted']
    ordering = ['id']

    def save_model(self, request, obj, form, change):
        obj.last_updated_by_new = request.user
        super().save_model(request, obj, form, change)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    fields = ['department','faculty']
    list_display = ['department','faculty','deleted','last_updated_by','created']
    list_editable = ['faculty','deleted']

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
       return queryset.update(deleted='Y')

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    fields = ['programme_id','programme','department','required_cteup','required_ctcup','deleted']
    list_display = ['programme_id','programme','department','required_cteup','required_ctcup','deleted','created']
    list_editable = ['programme','department']

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    fields = ['programme','course_code','status','course_reg_level','semester']
    list_display = ['programme','course_code','status','course_reg_level','semester'
    ,'register_flag','deleted','last_updated_by_new','created']
    list_editable = ['status','register_flag','deleted']

    def save_model(self, request, obj, form, change):
        obj.last_updated_by_new = request.user
        super().save_model(request, obj, form, change)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # fields = ['matric_number','surname','firstname']
    list_display = ['matric_number','surname','firstname','prog_code','status','acad_status','gpa','cgpa','last_updated_by_new',]
    # list_editable = ['acad_status']
    search_fields = ('matric_number','surname','firstname',)
    ordering = ('matric_number','surname',)
    list_per_page = 100
    readonly_fields = ['matric_number','last_updated_by_new']

admin.site.register(ErrorLog)
admin.site.register(History1)
admin.site.register(Lecturer)
admin.site.register(OutstandException)
admin.site.register(RegSummary)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    fields = ['matric_number_fk','course_code','status','semester']
    list_display = ['matric_number_fk','course_code','session_id','semester','status','score'
    ,'last_updated_by_new','deleted','created']
    list_editable = ['deleted']
    search_fields = ('matric_number_fk','course_code',)
    ordering = ('session_id','matric_number_fk',)
    list_per_page = 100

admin.site.register(RunregTransHistory)
admin.site.register(Session)

