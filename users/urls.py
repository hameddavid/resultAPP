from django.urls import  path, include
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.userlogin, name='userlogin'),
    path('master-sheet', views.display_class_master_sheet_exam, name='master_sheet'),
    path('master-sheet-sum', views.display_class_master_sheet_summary_exam, name='master_sheet_sum'),
    path('user/view-lecturer-roles', views.view_lecturer_roles_in_dpt, name='view_lecturer_roles'),
    # path('is_staff', views.is_staff, name='is_staff'),
    # path('forgot', views.forgotPasswordPage, name='forgotPage'),
    # path('register', views.registerPage, name='registerPage'),
    path('logout', views.logoutUser, name='logoutUser'),
    path('otp', views.otp, name='otp'),
    path('semester-activation', views.semester_activation, name='semester_activation'),
    path('validateOtp', views.validateOtp, name='validateOtp'),
    path('user/dashboard', views.dashboard, name='dashboard'),
    path('user-api/', include('users.api.urls'))


]