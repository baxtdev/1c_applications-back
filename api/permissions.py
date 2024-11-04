from rest_framework import permissions

from apps.user.models import User
from apps.utils.utils import get_object_or_none,get_filter_object_or_none

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsSuperAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_superuser


class IsSalesman(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_salesman or request.user.is_superuser    
    

class ClientPermission(permissions.BasePermission):
    """
    Custom permission to allow only clients to perform POST requests.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.CLIENT  or request.user.is_superuser    
    