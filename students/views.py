from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .serializers import StudentselfProfileSerializer, StudentEnrolledCourseSerializer
from .permission import IsStudent
from core.models import Course

class StudentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentselfProfileSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(tags=["Studeent can view Profile"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Student can update Profile"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
      
    @swagger_auto_schema(tags=["Student can partially update Profile"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)  

class StudentEnrolledCoursesView(generics.ListAPIView):
    serializer_class = StudentEnrolledCourseSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Course.objects.filter(students=self.request.user)

    @swagger_auto_schema(tags=["Student can view Enrolled Courses"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
