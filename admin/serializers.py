# serializers.py
from rest_framework import serializers
from core.models import User
from core.models import Course, User, CourseTeacher , CourseSchedule

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
        user = User.objects.create_user(**validated_data)
        return user


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        
        
class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=User.objects.filter(role='teacher'),
        required=False  
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'duration', 'teachers', 'created_at', 'updated_at']

    def create(self, validated_data):
        teachers = validated_data.pop('teachers', None)
        course = Course.objects.create(**validated_data)
        if teachers:
            for teacher in teachers:
                CourseTeacher.objects.create(course=course, teacher=teacher)
        return course

    def update(self, instance, validated_data):
        teachers = validated_data.pop('teachers', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if teachers is not None:  
            instance.teachers.clear()
            for teacher in teachers:
                CourseTeacher.objects.create(course=instance, teacher=teacher)
        return instance       


class CourseBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'duration']

class TeacherProfileSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'courses']

    def get_courses(self, obj):
        return CourseSerializer(obj.courses.all(), many=True).data
    
    
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'role', 'enrollment_year', 'batch', 'roll_number', 'is_active'
        ]
        read_only_fields = ['id', 'role'] 


class CourseScheduleSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = CourseSchedule
        fields = ['id', 'course', 'course_title', 'day_of_week', 'start_time', 'end_time', 'location']


