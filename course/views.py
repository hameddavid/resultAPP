from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from course.models import LecturerCourse, Course
from users.models import CustomUser
from base.models import Setting





@login_required(login_url='loginPage')
def my_courses(request):
    if request.method == "POST":
        if request.POST.getlist('courses') != []:
            settings = Setting.objects.get(status = 'ACTIVE')
            for course in request.POST.getlist('courses'): 
                LecturerCourse.objects.create(course = Course.objects.get(course_id = course),
                lecturer=CustomUser.objects.get(email='rafiua@run.edu.ng'),
                status=0,settings=settings)
        else:
            print("Not empty")
        try:
            pass
           
        except :
            pass
    courses = Course.objects.all()
    context = {'courses':courses}
    return render(request, 'course/courseform.html',context)


def addCourses(request):
    courses = Course.objects.all()
    return render(request, 'course/addCourses.html')


@login_required(login_url='loginPage')
def pendCourses(request):
    p_courses_lec = LecturerCourse.objects.filter(Q(lecturer=request.user) & Q(status=0)).values(
        "id","course","course_id__course_code","course_id__course_description","course_id__unit")
    context = {'p_courses_lec':p_courses_lec, 'count':p_courses_lec.count()}
    return render(request, 'course/pendingCourses.html',context)

@login_required(login_url='loginPage')
def approvedCourses(request):
    ap_courses_lec = LecturerCourse.objects.filter(Q(lecturer=request.user) & Q(status=10)).values(
        "id","course","course_id__course_code","course_id__course_description","course_id__unit")
    context = {'ap_courses_lec':ap_courses_lec, 'count':ap_courses_lec.count()}
    return render(request, 'course/approvedCourses.html',context)

