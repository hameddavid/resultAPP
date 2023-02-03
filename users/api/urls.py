from django.urls import  path
from . import views
from .views import UserApiView


urlpatterns = [
    path('all', views.user, name='user'),
    path('role', views.check_user_role_for_semester, name='role'),
    path('role/hod', views.check_user_role_in_semester_hod, name='role_hod'),
    path('broad', views.class_broadsheet_semester_session_list, name='broad'),
    path('ug-programmes', views.undergraduate_programme_list, name='ug_programmes'),
    # path('role/<int:pk>/', views.check_user_role_in_semester, name='role'),
    # path('all', UserApiView.as_view()),

]