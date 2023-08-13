from uuid import uuid4
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.accounts.models import User


def SendEmail(templateName, model, subject):
    html_body = render_to_string(templateName, {'model': model})
    plain_message = strip_tags(html_body)
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[model.email],
        html_message=html_body)


def ActivateCode(activeCode):
    try:
        user = User.objects.get(active_code=activeCode)
        if user.is_active:
            return False
        else:
            user.is_active = True
            user.active_code = str(uuid4()).replace('-', '')
            user.save()
            return True
    except User.DoesNotExist:
        return False
