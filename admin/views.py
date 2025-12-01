from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from admin.serializers import AdminCreateUserSerializer , UserNameSerializer
from drf_yasg.utils import swagger_auto_schema
from user.permissions import IsCustomAdmin
from rest_framework import generics
from core.models import User
from drf_yasg import openapi
from rest_framework import viewsets
from core.models import Course
from admin.serializers import CourseSerializer

class AdminCreateUserView(APIView):
    permission_classes = [IsCustomAdmin]
    
    @swagger_auto_schema(request_body=AdminCreateUserSerializer , tags=['Admin Create User'])  
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
        tags=['User List']
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

    @swagger_auto_schema(tags=["Courses List"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Creates a Course"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Get Course Details"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Update Course"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Partial Update Course"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Delete Course"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)