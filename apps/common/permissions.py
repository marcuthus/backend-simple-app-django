from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Allows access only to admin users (role == 'ADMIN', is_staff, or is_superuser).
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(
            getattr(request.user, 'role', '') == 'ADMIN'
            or request.user.is_staff
            or request.user.is_superuser
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to allow owners of an object or admins to edit/view it.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Admin has full access
        if (
            getattr(request.user, 'role', '') == 'ADMIN'
            or request.user.is_staff
            or request.user.is_superuser
        ):
            return True

        # Check if the target object is the user itself or belongs to user
        if hasattr(obj, 'id'):
            return str(obj.id) == str(request.user.id)
        if hasattr(obj, 'user_id'):
            return str(obj.user_id) == str(request.user.id)
        if hasattr(obj, 'user'):
            return str(obj.user.id) == str(request.user.id)

        return False
