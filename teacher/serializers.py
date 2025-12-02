from rest_framework import serializers
from core.models import User , CourseSchedule, Course

class TeacherOwnProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)  

    class Meta:
        model = User
        
        fields = ['username', 'email', 'first_name', 'last_name', 'department', 'role']
        read_only_fields = ['role']  


class CourseScheduleSerializerTeacher(serializers.ModelSerializer):
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = CourseSchedule
        fields = ['id', 'day_of_week', 'day_of_week_display', 'start_time', 'end_time', 'location']

class TeacherAssignedCourseSerializer(serializers.ModelSerializer):
    schedules = CourseScheduleSerializerTeacher(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'duration', 'schedules']