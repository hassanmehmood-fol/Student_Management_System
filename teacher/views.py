from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .serializers import TeacherOwnProfileSerializer
from .permissions import IsTeacherAndOwner
from core.models import User

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
