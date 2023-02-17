from django.http import HttpResponse, JsonResponse
from django.template import Template, Context
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.db.models import Q,Prefetch
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from base.models import Staff
from users import helpers
from base.baseHelper import session_semester_config, session_semester_config_always
from users.userForm import UserForm
from users.models import User,LogUserRoleForSemester
import json, os, re,random,string
from django.forms.models import model_to_dict
from undergraduate.models import Course, Curriculum,Student,Department,Programme,RegSummary,Student,Registration
from collections import Counter


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='index')
def view_lecturer_in_dpt(request):
    pass


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='index')
def view_lecturer_roles_in_dpt(request):
    curr_semester = session_semester_config()
    # owner, semester_session, programme, department, approved_by
    # .filter(~Q(a=True), x=5)
    lec_roles = LogUserRoleForSemester.objects.select_related('owner','programme').filter(department=request.user.department,
     semester_session=curr_semester.id).exclude(owner=request.user)
    
    return render(request, 'hod/lecturer_roles_in_dpt.html', context={'roles':lec_roles})




