from django.urls import  path

from .ug_lecturer_api_view import (lecturer_course_view,
class_broadsheet_semester_session_list,undergraduate_programme_list,
undergraduate_course_list,undergraduate_course_list_curriculum_base)
from .ug_api_hod_view import(get_user_courses_in_semester_for_approval,approve_disapprove_user_courses_in_semester)
from .reg_api_view import (submit_student_reg_score)


urlpatterns = [
    path('lec_course/', lecturer_course_view, name='lecturer_course_view'),
       path('broad', class_broadsheet_semester_session_list, name='broad'),
    path('ug-programmes',undergraduate_programme_list , name='ug_programmes'),
    path('ug-course-list',undergraduate_course_list, name='ug_course_list'),
    path('ug-course-list-curr-based',undergraduate_course_list_curriculum_base , name='ug_course_list_curr_based'),
    path('get-user-courses-in-semester-for-approval',get_user_courses_in_semester_for_approval , name='get_user_courses_in_semester_for_approval'),
    path('approve-disapprove-user-courses-in-semester',approve_disapprove_user_courses_in_semester , name='approve_disapprove_user_courses_in_semester'),
    path('submit-student-reg-score',submit_student_reg_score , name='submit_student_reg_score'),
    # path('role/<int:pk>/', views.check_user_role_in_semester, name='role'),
    # path('all', UserApiView.as_view()),

]