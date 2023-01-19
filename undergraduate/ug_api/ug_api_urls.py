from django.urls import  path

from .ug_lecturer_api_view import lecturer_course_view


urlpatterns = [
    path('lec_course/', lecturer_course_view, name='lecturer_course_view'),
    # path('role/<int:pk>/', views.check_user_role_in_semester, name='role'),
    # path('all', UserApiView.as_view()),

]