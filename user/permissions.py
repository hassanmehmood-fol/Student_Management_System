from rest_framework.permissions import BasePermission

class IsCustomAdmin(BasePermission):
    """
    Allows access only to users with role='admin',
    regardless of is_staff value.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')
