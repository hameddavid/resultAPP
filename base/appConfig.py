from django.http import HttpResponse
from base.models import  Setting


def get_settings():
    try:
        settings = Setting.objects.get(status = 'ACTIVE')
        return settings
    except:
        return HttpResponse("Error fetching settings")