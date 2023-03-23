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
        active_semester = Setting.objects.filter(status = 'ACTIVE',semester_open_close=True).first()
        return active_semester
    except:
        pass




import requests

def check_network():
    try:
        response = requests.get('https://www.google.com')
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False