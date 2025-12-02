from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .serializers import TeacherOwnProfileSerializer ,TeacherAssignedCourseSerializer
from .permissions import IsTeacherAndOwner
from core.models import Course , User
from teacher.permissions import IsTeacherAndOwner

class TeacherProfileView(generics.RetrieveUpdateAPIView):
    """
    View/Edit own profile (Teacher only).
    Email is non-editable.
    """
    serializer_class = TeacherOwnProfileSerializer
    permission_classes = [IsAuthenticated, IsTeacherAndOwner]

    def get_object(self):
      
        return self.request.user

    @swagger_auto_schema(tags=["Teacher Profile"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Teacher Profile"])
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Teacher Profile"])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class TeacherAssignedCoursesView(generics.ListAPIView):
    serializer_class = TeacherAssignedCourseSerializer
    permission_classes = [IsAuthenticated, IsTeacherAndOwner]

    @swagger_auto_schema(tags=["Teacher Profile"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
    
        return Course.objects.filter(teachers=self.request.user)