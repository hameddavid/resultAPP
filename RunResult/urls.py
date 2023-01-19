
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('ug/', include('undergraduate.urls')),
    path('base/', include('base.urls')),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'),name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns