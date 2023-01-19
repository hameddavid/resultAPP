from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from undergraduate.models import Course,Curriculum,LecturerCourse
from users.models import User
from base.models import Setting
from base.baseHelper import session_semester_config, session_semester_config_always




@login_required(login_url='index')
def my_courses(request):
    if request.method == "POST":
        if request.POST.getlist('courses') != []:
            for course in request.POST.getlist('courses'): 
                LecturerCourse.objects.create(course = Course.objects.get(course_id = course),
                lecturer=User.objects.get(email='rafiua@run.edu.ng'),
                status=0,settings=session_semester_config().id)
        else:
            print("Not empty")
        try:
            pass
           
        except :
            pass
    courses = Course.objects.all()
    context = {'courses':courses}
    return render(request, 'course/courseform.html',context)



@login_required(login_url='index')
def addCourses(request):
    unique_courses = []
    used_course_code = []
    curriculum = Curriculum.objects.filter(programme=request.user.programme, semester=session_semester_config().semester_code)
    for curr in curriculum:
        course = Course.objects.filter(course_code=curr.course_code).order_by('-unit_id').first()
        if course is not None:
            if course.course_code not in used_course_code:
                unique_courses.append(course)
                used_course_code.append(course.course_code )

    context = {"courses":unique_courses, "settings":session_semester_config()}
    return render(request, 'course/addCourses.html', context)


@login_required(login_url='index')
def pendCourses(request):
    unique_courses = []
    used_course_code = []
    p_courses_lec = LecturerCourse.objects.filter(Q(lecturer=request.user)  & Q(status='PENDING') & Q(settings=session_semester_config())) 
    for curr in p_courses_lec:
        course = Course.objects.filter(course_code=curr.course_code).order_by('-unit_id').first()
        if course is not None:
            if course.course_code not in used_course_code:
                unique_courses.append(course)
                used_course_code.append(course.course_code )
    context = {'p_courses_lec':unique_courses, 'count':p_courses_lec.count()}
    return render(request, 'course/pendingCourses.html',context)


@login_required(login_url='index')
def approvedCourses(request):
    unique_courses = []
    used_course_code = []
    p_courses_lec = LecturerCourse.objects.filter(Q(lecturer=request.user)  & Q(status='APPROVED') & Q(settings=session_semester_config())) 
    for curr in p_courses_lec:
        course = Course.objects.filter(course_code=curr.course_code).order_by('-unit_id').first()
        if course is not None:
            if course.course_code not in used_course_code:
                unique_courses.append(course)
                used_course_code.append(course.course_code )
    context = {'p_courses_lec':unique_courses, 'count':p_courses_lec.count()}
    return render(request, 'course/approvedCourses.html',context)
