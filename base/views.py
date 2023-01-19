from django.http import HttpResponse, JsonResponse
from django.template import Template, Context
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Staff, Setting
from users.userForm import UserForm
from users.models import User
from course.models import LecturerCourse,Course
import json, os, re








def insert_json(request):
    return JsonResponse({'res':'Do not try again to avoid duplicate entries'})
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    with open('base\data.json', encoding="utf8") as f:
        data = json.load(f)
    res = []
    for datum in data:
        if re.fullmatch(regex, datum['email']):
            res.append("Valid email")
            row = Staff(**datum)
            row.save()
    return JsonResponse({'res':res})
    #     print(datum['staff_no'])
    #     t = Template('<h1>test: {{data}} </h1>')
    #     c = Context({'data': datum['staff_no']})
    # return HttpResponse(t.render(c))

def testpage(request):
    request.session['test'] = int(request.session.get('test',0))+1
    user = User.objects.all()
    user = Staff.objects.all()
    t = Template('<h1>test: {{test}} </h1>')
    # c = Context({'test': request.session['test']})
    c = Context({'test': user})
    return HttpResponse(t.render(c))

def check_request_from_model_query(model , param, type):
    try:
        res = None
        if type == "EMAIL":
            res = model.objects.filter(email=param).first()
            if res is None:
                return None   
        return res   
    except:
        return JsonResponse({'data':'EXCEPT ERROR VERIFYING STAFF'})
       



def is_staff(request):
    try:
        email = request.POST.get('username').lower()
        staff = check_request_from_model_query(Staff,email, type='EMAIL')
        if staff is None:
            return JsonResponse({'status':'nok','data':'NOT_STAFF'})
        else:
            return JsonResponse({'status':'ok','data':'IS_STAFF'})
    except:
        return JsonResponse({'status':'nok','data':'EXCEPT ERROR VERIFYING STAFF'})

def otp(request):
    return render(request, 'base/otp.html')

def loginPage(request):
    
    if request.user.is_authenticated:
            return redirect('dashboard')
    if request.method == 'POST':
        return redirect('otp')
        try:
            email = request.POST.get('username').lower()
            password = request.POST.get('password')
            user = User.objects.filter(email=email).first()
            if user is None:
                    settings = Setting.objects.filter(status = 'ACTIVE').first()
                    if settings is None:
                        return JsonResponse({'status':'nok','msg':'NO CURRENT ACTIVE SESSION'})
                    save_user = User.objects.create_user(
                                email = request.POST.get('email'), 
                                password = request.POST.get('password'), 
                                role =  {settings.id:['LEC']},
                                is_active = False)
                    save_user.save()
                    # send OTP 
                    # signal to link staff with user
                    #  redirect to OTP page  

                
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                request.session['pendCourses'] = LecturerCourse.objects.filter(Q(lecturer=request.user) & Q(status=0)).count()
                request.session['appCourses'] = LecturerCourse.objects.filter(Q(lecturer=request.user) & Q(status=10)).count()
                return redirect('dashboard')
            else:
                messages.error(request, 'Username OR password does not exit')
        except:
            messages.error(request, 'User does not exist')

    context = {}
    return render(request, 'base/login.html', context)



def forgotPasswordPage(request):
    context = {}
    return render(request, 'base/forgot.html', context)


def registerPage(request):
    if request.method == "POST":
      
    #    try:
            validate_email = Staff.objects.filter(email = request.POST.get('email')).first()
            settings = Setting.objects.filter(status = 'ACTIVE').first()
            if validate_email is None or settings is None:
                messages.error(request, f'(Email does noy exist  or settings issue)!')
                return redirect('registerPage')
            # user_profile = StaffProfile.objects.get(staff_id = validate_email.userid)
            
            messages.error(request, 'Woking .........')
            return redirect('registerPage')
            if request.POST.get('password') != request.POST.get('password_confirmation'):
                messages.error(request, 'Confirm password does not match!')
                return redirect('registerPage')

            save_user = User.objects.create_user(
            email = request.POST.get('email'), 
            password = request.POST.get('password'), 
            role =  {settings.id:['LEC']},
            is_active = True)
            save_user.save()
            # , my_approved_courses = {settings.id:[]}
            # title = user_profile.title,
            # staff_no  = user_profile.staff_no, sh_staff_no = user_profile.sh_staff_no,
            # firstname = user_profile.firstname , middlename = user_profile.middlename,
            # lastname = user_profile.lastname, phone = validate_email.phone,
            # profile_image = validate_email.profile_image, 
            # profile_image_small = validate_email.profile_image_small,
            # signature = user_profile.signature, 
            # retired =  validate_email.retired,adjunct =  validate_email.adjunct,
            # disengaged =  validate_email.disengaged,
            # staff =   validate_email, 
            # progId =  {settings.id:[]},level =  {settings.session:[]} ,
            messages.success(request, 'Account created successfully!')
            return redirect('loginPage')
    #    except:
    #         messages.error(request, 'Error creating new account ( email already exist  or not RUN email )!')
    #         return redirect('registerPage')

    context = {}
    return render(request, 'base/register.html', context)


@login_required(login_url='loginPage')
def dashboard(request):
    context = {}
    return render(request, 'base/dashboard.html', context)



def logoutUser(request):
    if 'pendCourses' in request.session:
        del request.session['pendCourses']
    if 'appCourses' in request.session:
        del request.session['appCourses']
    logout(request)
    return redirect('loginPage')



@login_required(login_url='loginPage')
def testUser(request):
    settings = Setting.objects.get(status = 'ACTIVE')
    data = dict(request.user.my_approved_courses)[f"{settings.id}"]
    myCourses = Course.objects.filter(course_id__in=data)
    print(myCourses)
    context = {'mycourses':myCourses}
    return render(request, 'base/testUser.html', context)


def addRole(request):
    return JsonResponse({"created":"success"})
    
    pass

# https://books.agiliq.com/projects/django-orm-cookbook/en/latest/distinct.html
# distinct = User.objects.values(
#     'first_name'
# ).annotate(
#     name_count=Count('first_name')
# ).filter(name_count=1)
# records = User.objects.filter(first_name__in=[item['first_name'] for item in distinct])

# User.objects.distinct("first_name").all()