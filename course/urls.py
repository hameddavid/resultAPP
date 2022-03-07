from django.urls import  path, include
from . import views
from . import api
urlpatterns = [
   
    # path('', views.courseHome, name='course'),
    path('mycourse', views.my_courses, name='mycourse'),
    path('add_courses', views.addCourses, name='add_courses'),
    path('approved_coures', views.approvedCourses, name='approved_courses'),
    path('pending_courses', views.pendCourses, name='pending_courses'),
    path('api', include('course.api.api_urls')),
    # path('testuser', views.testUser, name='testuser'),
    # path('about/', views.about, name='about'),
    # path('profile/<str:pk>/', views.user_profile, name='userprofile'),
]

