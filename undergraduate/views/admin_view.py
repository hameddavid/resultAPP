
from django.shortcuts import render,redirect



def admin_reg_activities(request):
    if  request.user.is_superuser or  request.user.is_admin:
        
        return render(request, 'admin/reg_activities.html')
    
    return redirect('dashboard')

    