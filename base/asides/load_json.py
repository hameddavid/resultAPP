import json
from models import Staff

with open('data.json') as f:
  data = json.load(f)

for datum in data:
    # row = Staff(**datum)
    # row.save()
    print(datum['staff_no'])


  

# https://gist.github.com/LowerDeez/9a8b30428a96c4b965d059925a7bd659
# from django.core.mail import EmailMessage
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.template import Context
# from django.template.loader import get_template

# from app.settings import EMAIL_ADMIN
# from .models.order import Order


# @receiver(post_save, sender=Order)
# def send_order_email_confirmation(sender, instance, **kwargs):
#     """
#     Send email to customer with order details.
#     """
#     order = instance
#     message = get_template("emails/order_conf.html").render(Context({
#         'order': order.get_serialized_data()
#     }))
#     mail = EmailMessage(
#         subject="Order confirmation",
#         body=message,
#         from_email=EMAIL_ADMIN,
#         to=[order.email],
#         reply_to=[EMAIL_ADMIN],
#     )
#     mail.content_subtype = "html"
#     return mail.send()
    