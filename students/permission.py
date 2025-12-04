from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    """
    Allows access only to authenticated users with role='student'.
    """

    def has_permission(self, request, view):
        # User must be authenticated AND role must be 'student'
        return bool(request.user and request.user.is_authenticated and request.user.role == 'student')

    def has_object_permission(self, request, view, obj):
        # Ensure user can only access their own object
        return obj == request.user
