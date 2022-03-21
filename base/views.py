
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Staff, StaffProfile, Setting
from users.userForm import UserForm
from users.models import CustomUser



def loginPage(request):
    if request.user.is_authenticated:
            return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(email=email) 
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
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
      
       try:
            validate_email = Staff.objects.get(email = request.POST.get('email'))
            user_profile = StaffProfile.objects.get(staff_id = validate_email.userid)
            settings = Setting.objects.get(status = 'ACTIVE')
            
            if request.POST.get('password') != request.POST.get('password_confirmation'):
                messages.error(request, 'Confirm password does not match!')
                return redirect('registerPage')

            save_user = CustomUser.objects.create_user(email = request.POST.get('email'), password = request.POST.get('password'), title = user_profile.title,
            staff_no  = user_profile.staff_no, sh_staff_no = user_profile.sh_staff_no,firstname = user_profile.firstname , middlename = user_profile.middlename,
            lastname = user_profile.lastname, phone = validate_email.phone,profile_image = validate_email.profile_image, profile_image_small = validate_email.profile_image_small,
            signature = user_profile.signature, retired =  validate_email.retired,adjunct =  validate_email.adjunct, disengaged =  validate_email.disengaged,
            staff =   validate_email, role =  {settings.id:['LEC']}, my_approved_courses = {settings.id:[]},
            progId =  {settings.id:[]},level =  {settings.session:[]} ,is_active = True)
            save_user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('loginPage')
       except:
            messages.error(request, 'Error creating new account ( email already exist  or not RUN email )!')
            return redirect('registerPage')

    context = {}
    return render(request, 'base/register.html', context)


@login_required(login_url='loginPage')
def dashboard(request):
    context = {}
    return render(request, 'base/dashboard.html', context)



def logoutUser(request):
    logout(request)
    return redirect('loginPage')



@login_required(login_url='loginPage')
def testUser(request):
    data = request.user.my_approved_courses
    print(data.get('3'))
    context = {}
    return render(request, 'base/testUser.html', context)

# https://books.agiliq.com/projects/django-orm-cookbook/en/latest/distinct.html
# distinct = User.objects.values(
#     'first_name'
# ).annotate(
#     name_count=Count('first_name')
# ).filter(name_count=1)
# records = User.objects.filter(first_name__in=[item['first_name'] for item in distinct])

# User.objects.distinct("first_name").all()