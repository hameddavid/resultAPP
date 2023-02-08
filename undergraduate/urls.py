from django.urls import  path, include
from .ug_api.ug_api_views import (SettingApiView,loadJson,loadRegistrationsJson)
from .views import course_view, reg_view


urlpatterns = [

    #  path('api', SettingApiView.as_view()),
     path('load-json', loadJson),
     path('load-reg', loadRegistrationsJson),

    path('mycourse', course_view.my_courses, name='mycourse'),
    path('add_courses', course_view.addCourses, name='add_courses'),
    path('approved_coures', course_view.approvedCourses, name='approved_courses'),
    path('pending_courses', course_view.pendCourses, name='pending_courses'),
    path('get_student_reg', reg_view.get_student_reg, name='get_student_reg'),
  


    path('api/', include('undergraduate.ug_api.ug_api_urls')),

]


