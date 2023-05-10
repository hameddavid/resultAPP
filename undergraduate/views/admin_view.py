
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required



@login_required(login_url='index')
def admin_reg_activities(request):
    if request.user.email in ['olaitanf@run.edu.ng','hamendment@gmail.com']:
        return render(request, 'admin/admin_activities.html')
    
    return redirect('dashboard')

    