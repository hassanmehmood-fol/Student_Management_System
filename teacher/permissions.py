from rest_framework.permissions import BasePermission

class IsTeacherAndOwner(BasePermission):
    def has_permission(self, request, view):
      
        return request.user.is_authenticated and request.user.role == 'teacher'

    def has_object_permission(self, request, view, obj):
        
        return obj == request.user
