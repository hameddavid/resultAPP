from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from django.contrib import messages
from django.shortcuts import redirect
from django.template import Context
from django.conf import settings


def semester_activation_email(data):
    try:
        message = get_template('user/email/account_activate.html').render({'data':data})
        email = EmailMessage(f'{data.semester_session_id.semester_name} {data.semester_session_id} ACCOUNT VERIFICATION::RUNRESULT',message,settings.EMAIL_HOST_USER,[data.email])
        email.fail_silently = True
        email.send() 
    except :
        # messages.error(request,'Error sending email for semester activation')
        return redirect('index')

