from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для пользователей c правами администратора или на чтение."""

    def has_permission(self, request, view):
        return (
                request.user.is_authenticated and
                request.user.is_superuser and
                request.user.is_active or
                request.method in permissions.SAFE_METHODS
        )
