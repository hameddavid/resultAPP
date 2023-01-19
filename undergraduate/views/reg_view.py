from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from undergraduate.models import (Course,Curriculum,LecturerCourse,Registration)
from users.models import User
from base.models import Setting
from base.baseHelper import session_semester_config, session_semester_config_always




@login_required(login_url='index')
def get_student_reg(request):
    if request.POST.get('course_code') is not None:
        regs = Registration.objects.filter( Q(course_code=request.POST.get('course_code')) & Q(semester=session_semester_config().semester_code) & Q(session_id=session_semester_config().session))
        context = {'regs':regs, 'count':regs.count(), 'course':request.POST.get('course_code')}
        return render(request, 'course/studReg.html', context)
    else :
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'approved_coures'))

