from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from undergraduate.models import (Course,Curriculum,LecturerCourse,Registration)
from users.models import User
from base.models import Setting
from base.baseHelper import session_semester_config, session_semester_config_always


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='index')
def view_lecturer_courses_in_semester(request):  
    # lecturer programme course_code   status
    curr_semester = session_semester_config()
    lec_course= LecturerCourse.objects.select_related('lecturer','settings').filter(department=request.user.department,
     settings=curr_semester.id).distinct('lecturer')
    
    return render(request, 'hod/lecturer_courses_in_dpt_in_semester.html', context={'roles':lec_course})



