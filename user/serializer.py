
from rest_framework import serializers
from django.contrib.auth import authenticate
from core.models import User
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework import serializers
from core.models import User
import re

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'},
        min_length=6,  
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'first_name', 'last_name']

    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value


    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        if not re.match("^[A-Za-z0-9_]+$", value):
            raise serializers.ValidationError("Username can only contain letters, numbers, and underscores.")
        return value
      
    def validate_role(self, value):
        allowed_roles = [choice[0] for choice in User.ROLE_CHOICES]
        if value not in allowed_roles:
            raise serializers.ValidationError(f"Role must be one of {allowed_roles}.")
        return value
      
    def validate(self, attrs):
        password = attrs.get('password')
        if password:
            if not re.search(r'[A-Z]', password):
                raise serializers.ValidationError("Password must contain at least one uppercase letter.")
            if not re.search(r'[a-z]', password):
                raise serializers.ValidationError("Password must contain at least one lowercase letter.")
            if not re.search(r'\d', password):
                raise serializers.ValidationError("Password must contain at least one digit.")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise serializers.ValidationError("Password must contain at least one special character.")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'student'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()  # use email instead of username
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username  # get username from email
            except User.DoesNotExist:
                raise serializers.ValidationError("No user found with this email.")

            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                data['access'] = str(refresh.access_token)
                data['refresh'] = str(refresh)
                data['user'] = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                }
                return data
            else:
                raise serializers.ValidationError("Unable to login with provided credentials.")
        else:
            raise serializers.ValidationError("Must include email and password.")
