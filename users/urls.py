from django.urls import  path, include
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.userlogin, name='userlogin'),
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