from rest_framework import serializers
from core.models import User
import random
import string
from django.core.mail import send_mail
from django.conf import settings

class AdminCreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'first_name', 'last_name']
        
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
          raise serializers.ValidationError("Username already exists.")
        return value
    
    
    def validate_role(self, value):
        allowed_roles = ['student', 'teacher']
        if value not in allowed_roles:
            raise serializers.ValidationError(f"Role must be one of {allowed_roles}")
        return value

    def create(self, validated_data):
      
        password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=8))
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            role=validated_data['role'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
      
        from django.core.mail import send_mail
        send_mail(
            subject='Your Account Created',
            message=f"Hello {user.username},\n\nYour account has been created.\nEmail: {user.email}\nPassword: {password}\n\nPlease login and change your password.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user
