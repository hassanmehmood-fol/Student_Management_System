from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import CourseSchedule , Course , Enrollment

User = get_user_model()

class StudentselfProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'enrollment_year', 'batch', 'roll_number', 'password']
        read_only_fields = ['email', 'enrollment_year', 'batch', 'roll_number', 'username']

    def update(self, instance, validated_data):
        # Update first_name & last_name
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # Update password if provided
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance



class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']



class CourseScheduleSerializerStudents(serializers.ModelSerializer):
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)

    class Meta:
        model = CourseSchedule
        fields = ['id', 'day_of_week', 'day_of_week_display', 'start_time', 'end_time', 'location', 'teacher_name']
        
        

class StudentEnrolledCourseSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, read_only=True)
    schedules = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'duration', 'teachers', 'schedules']

    def get_schedules(self, obj):
        qs = obj.schedules.all()  # all schedules of the course
        return CourseScheduleSerializerStudents(qs, many=True).data
        
