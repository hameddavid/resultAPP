from django.urls import  path

from .base_api_view import loadCSV



urlpatterns = [
    path('load-csv', loadCSV),

]