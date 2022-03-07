from django.urls import  path
from . import views

urlpatterns = [
    path('', views.loginPage, name='loginPage'),
    path('forgot', views.forgotPasswordPage, name='forgotPage'),
    path('register', views.registerPage, name='registerPage'),
    path('logout', views.logoutUser, name='logoutUser'),
    path('dashboard', views.dashboard, name='dashboard'),




    path('testuser', views.testUser, name='testuser'),
    # path('about/', views.about, name='about'),
    # path('profile/<str:pk>/', views.user_profile, name='userprofile'),
]

