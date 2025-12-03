from rest_framework import serializers
from core.models import User , CourseSchedule, Course , Enrollment

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
    schedules = serializers.SerializerMethodField()  # use SerializerMethodField

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'duration', 'schedules']

    def get_schedules(self, obj):
        user = self.context['request'].user
        qs = obj.schedules.filter(teacher=user)  # only schedules for this teacher
        return CourseScheduleSerializerTeacher(qs, many=True).data



class StudentEnrollmentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='student.username', read_only=True)
    email = serializers.EmailField(source='student.email', read_only=True)
    status = serializers.CharField()
    enrolled_at = serializers.DateTimeField()

    class Meta:
        model = Enrollment
        fields = ['username', 'email', 'status', 'enrolled_at']
        


class TeacherCourseWithStudentsSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()  # Ye uncomment karo

    class Meta:
        model = Course
        fields = ['students']  # students bhi fields me hona chahiye

    def get_students(self, obj):
        user = self.context['request'].user

        # Sirf enrollments jo teacher ke courses me ho
        enrollments = obj.enrollments.all()
    
        if user.role == 'teacher' and user not in obj.teachers.all():
            return []
        
        return StudentEnrollmentSerializer(enrollments, many=True, context={'request': self.context.get('request')}).data



class StudentDetailSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'enrollment_year', 'batch', 'roll_number', 'courses']

    def get_courses(self, obj):
        # Only courses taught by the requesting teacher
        teacher = self.context['request'].user
        courses = obj.courses_enrolled.filter(teachers=teacher)
        return [{'id': c.id, 'title': c.title} for c in courses]


class TeacherEnrollStudentSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(write_only=True)
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student_username', 'course_id', 'status', 'enrolled_at']
        read_only_fields = ['id', 'enrolled_at']

    def validate(self, attrs):
        student_username = attrs.get('student_username')
        course_id = attrs.get('course_id')

        try:
            student = User.objects.get(username=student_username, role='student')
        except User.DoesNotExist:
            raise serializers.ValidationError("Student not found or not a student.")

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course not found.")

        # Check if teacher owns the course
        request_user = self.context['request'].user
        if not course.teachers.filter(id=request_user.id).exists():
            raise serializers.ValidationError("You are not authorized to enroll students in this course.")

        # Check if student already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("Student is already enrolled in this course.")

        attrs['student'] = student
        attrs['course'] = course
        return attrs

    def create(self, validated_data):
        return Enrollment.objects.create(
            student=validated_data['student'],
            course=validated_data['course'],
            status=validated_data.get('status', 'active')
        )
