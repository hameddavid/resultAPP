from django.urls import  path, include
from .ug_api.ug_api_views import (SettingApiView,loadJson_reg_summary,
                    loadRegistrationsJson,correct_prog_dpt_diff,loadJson_reg,
                    loadJson_courses,loadJson_cur,loadJson_student,loadJson_prog,manage_course_reg)
from . import views





urlpatterns = [
    #  path('api', SettingApiView.as_view()),
    path('manage-course-reg', manage_course_reg),
    path('load-json-reg-sum', loadJson_reg_summary),
    path('load-json-prog', loadJson_prog),
    path('load-json-reg', loadJson_reg),
    path('load-json-courses', loadJson_courses),
    path('load-json-cur', loadJson_cur),
    path('load-json-stud', loadJson_student),
    path('load-stud-reg', loadRegistrationsJson),
    path('load-correction', correct_prog_dpt_diff),
    path('mycourse', views.my_courses, name='mycourse'),
    path('add_courses', views.addCourses, name='add_courses'),
    path('approved_coures', views.approvedCourses, name='approved_courses'),
    path('pending_courses', views.pendCourses, name='pending_courses'),
    path('get_student_reg', views.get_student_reg, name='get_student_reg'),
    path('get-print-result-view', views.get_print_result_view, name='get_print_result_view'),
    path('view-lecturer-courses-in-semester', views.view_lecturer_courses_in_semester, name='view_lecturer_courses_in_semester'),
    

    # path('master-sheet', result_view.display_class_master_sheet_exam, name='master_sheet'),
    # path('master-sheet-sum', result_view.display_class_master_sheet_summary_exam, name='master_sheet_sum'),
    # path('master-sheet-sum-2', result_view.display_class_master_sheet_summary_exam_direct_from_reg_table, name='master_sheet_sum_2'),
    path('get-broadsheet-or-summary-for-print', views.get_broadsheet_or_summary_for_print, name='get_broadsheet_or_summary_for_print'),

    path('admin-activities', views.admin_reg_activities, name='admin_reg_activities'),

    path('api/', include('undergraduate.ug_api.ug_api_urls')),

]


