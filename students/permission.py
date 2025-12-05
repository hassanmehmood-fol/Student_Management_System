from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    """
    Allows access only to authenticated users with role='student'.
    """

    def has_permission(self, request, view):
        
        return bool(request.user and request.user.is_authenticated and request.user.role == 'student')

    def has_object_permission(self, request, view, obj):
      
        return obj == request.user
