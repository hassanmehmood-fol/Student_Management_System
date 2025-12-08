# serializers.py
from rest_framework import serializers
from core.models import User
from core.models import Course, User, CourseTeacher , CourseSchedule , Enrollment
from .task import send_user_credentials_email 
import random, string

def generate_random_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

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
       
        password = generate_random_password()
        user = User.objects.create_user(password=password, **validated_data)
        send_user_credentials_email.delay(user.email, user.username, password)
        
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
    
    students = serializers.SerializerMethodField() 

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'duration', 'teachers', 'students', 'created_at', 'updated_at']
        
    def validate_title(self, value):
        queryset = Course.objects.filter(title__iexact=value)

        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError("This course title already exists.")

        return value
        

    def get_students(self, obj):
        return [en.student.username for en in obj.enrollments.all()]    


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
     
class TeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


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
        return CourseBriefSerializer(obj.courses.all(), many=True).data
        
class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name']
    
    
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'role', 'enrollment_year', 'batch', 'roll_number', 'is_active'
        ]
        read_only_fields = ['id', 'role'] 


class CourseScheduleSerializerAdmin(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)

    class Meta:
        model = CourseSchedule
        fields = ['id', 'course', 'course_title','teacher', 'teacher_name',  'day_of_week', 'start_time', 'end_time', 'location']


class EnrollmentSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(write_only=True)
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student_id', 'course_id', 'status', 'enrolled_at']
        read_only_fields = ['id', 'enrolled_at']

    def create(self, validated_data):
        student_id = validated_data.pop('student_id')
        course_id = validated_data.pop('course_id')

        try:
            student = User.objects.get(id=student_id, role='student')
        except User.DoesNotExist:
            raise serializers.ValidationError({"student_id": "Student not found or not a student."})

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError({"course_id": "Course not found."})

        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            course=course,
            defaults={'status': validated_data.get('status', 'active')}
        )
        
        if not created:
            raise serializers.ValidationError({"detail": "Student is already enrolled in this course."})

        return enrollment


class AssignTeacherSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField(required=True)

    def validate_teacher_id(self, value):
        from core.models import User
        try:
            teacher = User.objects.get(id=value, role='teacher')
        except User.DoesNotExist:
            raise serializers.ValidationError("Teacher not found or not a teacher.")
        return value
    