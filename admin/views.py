from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from admin.serializers import AdminCreateUserSerializer , UserNameSerializer , StudentProfileSerializer ,  CourseScheduleSerializer 
from drf_yasg.utils import swagger_auto_schema
from user.permissions import IsCustomAdmin
from rest_framework import generics
from core.models import User , CourseSchedule
from drf_yasg import openapi
from rest_framework import viewsets
from core.models import Course , CourseTeacher
from admin.serializers import CourseSerializer
from django.shortcuts import get_object_or_404
from admin.serializers import TeacherProfileSerializer , EnrollmentSerializer , AssignTeacherSerializer
from rest_framework.decorators import action

class AdminCreateUserView(APIView):
    permission_classes = [IsCustomAdmin]
    
    @swagger_auto_schema(request_body=AdminCreateUserSerializer , tags=['Create User (Teacher , Student) by Admin'])  
    def post(self, request):
        serializer = AdminCreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": {             
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserListView(generics.ListAPIView):
    serializer_class = UserNameSerializer
    permission_classes = [IsCustomAdmin]

    role_param = openapi.Parameter(
        'role',
        openapi.IN_QUERY,
        description="Filter users by role",
        type=openapi.TYPE_STRING,
        enum=['teacher', 'student'],
        required=False
    )

    @swagger_auto_schema(
        manual_parameters=[role_param],
        tags=['Admin Profile']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        role = self.request.query_params.get('role')
        queryset = User.objects.all()
        if role and role.lower() in ['student', 'teacher']:
            queryset = queryset.filter(role=role.lower())
        return queryset

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsCustomAdmin]

    @swagger_auto_schema(tags=["Display Courses List by Admin"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Add Course by Admin"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Course Details by Admin"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Update Course by Admin"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Partial Update Course by Admin"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Delete Course by Admin"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    
    @swagger_auto_schema(
        request_body=AssignTeacherSerializer,
        tags=["Assign Teacher to Course by Admin"]
    )
    @action(detail=True, methods=["post"], url_path="assign-teacher")
    def assign_teacher(self, request, pk=None):
        """
        Assign a teacher to this course.
        """
        course = self.get_object()
        serializer = AssignTeacherSerializer(data=request.data)
        if serializer.is_valid():
            teacher_id = serializer.validated_data["teacher_id"]
            teacher = User.objects.get(id=teacher_id)

            
            course_teacher, created = CourseTeacher.objects.get_or_create(
                course=course, teacher=teacher
            )

            if created:
                message = f"Teacher '{teacher.username}' assigned successfully!"
            else:
                message = f"Teacher '{teacher.username}' is already assigned to this course."

            return Response({"message": message}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
    
class TeacherProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Admin can view all teachers with their courses efficiently (prefetch_related).
    """
    queryset = User.objects.filter(role='teacher').prefetch_related('courses')
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsCustomAdmin]

    @swagger_auto_schema(tags=["Display Teachers List by Admin"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Teacher Detail Profile (Specific id) by Admin"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
        return teacher    
    
    
class StudentProfileViewSet(viewsets.ModelViewSet):
    """
    Admin can view, update, or delete student profiles
    """
    serializer_class = StudentProfileSerializer
    permission_classes = [IsCustomAdmin]

    def get_queryset(self):
        
        return User.objects.filter(role='student')
    
    @swagger_auto_schema(tags=["Display Students List by Admin"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Student Detail Profile (Specific id) by Admin"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Update Student Profile by Admin"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Partial Update Student Profile by Admin"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Delete Student Profile by Admin"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)    
    

class CourseScheduleViewSet(viewsets.ModelViewSet):
    """
    Admin can create, update, view, and delete course schedules
    """
    queryset = CourseSchedule.objects.all()
    serializer_class = CourseScheduleSerializer
    permission_classes = [IsCustomAdmin]

    @swagger_auto_schema(tags=["Admin Profile"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Admin Profile"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Admin Profile"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Admin Profile"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Admin Profile"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Admin Profile"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    
class EnrollStudentView(APIView):
    permission_classes = [IsCustomAdmin]

    @swagger_auto_schema(request_body=EnrollmentSerializer, tags=["Admin Profile"])
    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            enrollment = serializer.save()
            return Response({
                "message": "Student enrolled successfully!",
                "data": EnrollmentSerializer(enrollment).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    