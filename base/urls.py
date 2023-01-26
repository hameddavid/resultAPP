from django.urls import  path, include
from . import views, view_aside
from .seePackage import package

urlpatterns = [
    # path('', views.loginPage, name='loginPage'),
    # path('is_staff', views.is_staff, name='is_staff'),
    # path('forgot', views.forgotPasswordPage, name='forgotPage'),
    # path('register', views.registerPage, name='registerPage'),
    # path('logout', views.logoutUser, name='logoutUser'),
    # path('otp', views.otp, name='otp'),
    # path('dashboard', views.dashboard, name='dashboard'),




    path('testuser', views.testUser, name='testuser'),
    path('test_signal', view_aside.testSignalView, name='test-signal'),
    # path('about/', views.about, name='about'),
    # path('profile/<str:pk>/', views.user_profile, name='userprofile'),
    path('testpage', views.testpage, name='testpage'),
    path('testpack', package, name='testpack'),
    path('insert_json', views.insert_json, name='insert_json'),

    path('api/', include('base.api.base_api_urls')),
]

