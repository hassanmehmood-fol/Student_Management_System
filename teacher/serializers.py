from rest_framework import serializers
from core.models import User

class TeacherOwnProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)  

    class Meta:
        model = User
        
        fields = ['username', 'email', 'first_name', 'last_name', 'department', 'role']
        read_only_fields = ['role']  
