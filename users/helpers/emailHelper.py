from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from django.contrib import messages
from django.shortcuts import redirect
from django.template import Context
from django.conf import settings
import requests



from django.core.mail import send_mail

def send_email(data):
    subject = f'{data.semester_session_id.semester_name} {data.semester_session_id} ACCOUNT VERIFICATION::RUNRESULT'
    message = data.otp
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [data.email]
    sent_count = send_mail(subject, message, from_email, recipient_list, fail_silently=True)

    if sent_count == 1:
        return 'Email sent successfully'
    else:
        url = 'https://adms.run.edu.ng/codebehind/destEmail.php'
        payload = {"From":"ict@run.edu.ng",
         "FromName":"REDEEMER's UNIVERSITY",
         "To":data.email, "Recipient_names":data.email,"Msg":data.otp,"Subject":subject,"HTML_type":True}
        response = requests.post(url, data=payload)
        print("@@@@###############################@@@@@@@@@@@@@@")
        print("Content:", response.content)
        return response.status_code  # 200
        # return 'Email sending failed'




def semester_activation_email(data):
    try:
        message = get_template('user/email/account_activate.html').render({'data':data})
        email = EmailMessage(f'{data.semester_session_id.semester_name} {data.semester_session_id} ACCOUNT VERIFICATION::RUNRESULT',message,settings.EMAIL_HOST_USER,[data.email])
        email.fail_silently = True
        email.send() 
    except :
        # messages.error(request,'Error sending email for semester activation')
        return redirect('index')

