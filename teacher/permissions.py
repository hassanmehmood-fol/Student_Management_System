from rest_framework.permissions import BasePermission

class IsTeacherAndOwner(BasePermission):
    def has_permission(self, request, view):
        # Check if user is authenticated and is a teacher
        return request.user.is_authenticated and request.user.role == 'teacher'

    def has_object_permission(self, request, view, obj):
        # Check if the teacher is assigned to this course
        return obj.teachers.filter(id=request.user.id).exists()
