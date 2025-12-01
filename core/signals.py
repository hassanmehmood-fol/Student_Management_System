from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import User
from django.core.mail import send_mail
from django.conf import settings
import random
import string

@receiver(post_save, sender=User)
def send_user_creation_email(sender, instance, created, **kwargs):
    if created:
        # Generate random password
        password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=8))
        
        # Set password for the user
        instance.set_password(password)
        instance.save(update_fields=['password'])
        
        # Send email
        send_mail(
            subject='Your Account Created',
            message=f"Hello {instance.username},\n\nYour account has been created.\nEmail: {instance.email}\nPassword: {password}\n\nPlease login and change your password.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )
