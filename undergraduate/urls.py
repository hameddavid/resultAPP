from django.urls import  path, include
from .ug_api.ug_api_views import (SettingApiView,loadJson,
                    loadRegistrationsJson,correct_prog_dpt_diff,loadJson_reg,loadJson_courses,loadJson_cur)
from .views import course_view, reg_view, hod_view,result_view


urlpatterns = [
    #  path('api', SettingApiView.as_view()),
    path('load-json', loadJson),
    path('load-json-reg', loadJson_reg),
    path('load-json-courses', loadJson_courses),
    path('load-json-cur', loadJson_cur),
    path('load-reg', loadRegistrationsJson),
    path('load-correction', correct_prog_dpt_diff),
    path('mycourse', course_view.my_courses, name='mycourse'),
    path('add_courses', course_view.addCourses, name='add_courses'),
    path('approved_coures', course_view.approvedCourses, name='approved_courses'),
    path('pending_courses', course_view.pendCourses, name='pending_courses'),
    path('get_student_reg', reg_view.get_student_reg, name='get_student_reg'),
    path('get-print-result-view', result_view.get_print_result_view, name='get_print_result_view'),
    path('view-lecturer-courses-in-semester', hod_view.view_lecturer_courses_in_semester, name='view_lecturer_courses_in_semester'),
    

    # path('master-sheet', result_view.display_class_master_sheet_exam, name='master_sheet'),
    # path('master-sheet-sum', result_view.display_class_master_sheet_summary_exam, name='master_sheet_sum'),
    # path('master-sheet-sum-2', result_view.display_class_master_sheet_summary_exam_direct_from_reg_table, name='master_sheet_sum_2'),
    path('get-broadsheet-or-summary-for-print', result_view.get_broadsheet_or_summary_for_print, name='get_broadsheet_or_summary_for_print'),


    path('api/', include('undergraduate.ug_api.ug_api_urls')),

]


