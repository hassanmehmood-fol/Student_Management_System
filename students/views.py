from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import StudentselfProfileSerializer , StudentEnrolledCourseSerializer
from .permission import IsStudent
from core.models import Course

class StudentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentselfProfileSerializer
    permission_classes = [IsAuthenticated , IsStudent]

    def get_object(self):
        
        return self.request.user


class StudentEnrolledCoursesView(generics.ListAPIView):
    serializer_class = StudentEnrolledCourseSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Course.objects.filter(students=self.request.user)