from django.db.models.signals import post_save, pre_delete
# from django.contrib.auth.models import User
from users.models import User
from django.dispatch import receiver
from base.models import Staff
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.conf import settings


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
	if created:
		Staff.objects.filter(email=instance.email).update(user_id=instance)
		# message = get_template('user/email/account_activate.html').render({'data':instance})
		# email = EmailMessage('ACCOUNT VERIFICATION::RUNRESULT',message,settings.EMAIL_HOST_USER,['hamendment@gmail.com'])
		# email.fail_silently = True
		# email.send()

	

	
