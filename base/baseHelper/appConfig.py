from django.http import HttpResponse
from base.models import  Setting


def session_semester_config_always():
    try:
        active_semester = Setting.objects.filter(status = 'ACTIVE').first()
        if active_semester is None:
            return Setting.objects.all().last()
        return active_semester
    except:
        pass


def session_semester_config():
    try:
        active_semester = Setting.objects.filter(status = 'ACTIVE').first()
        return active_semester
    except:
        pass