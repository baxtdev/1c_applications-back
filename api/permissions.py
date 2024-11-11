from rest_framework import permissions

from apps.user.models import User
from apps.utils.utils import get_object_or_none,get_filter_object_or_none



class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role == User.ADMIN or user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.role == User.ADMIN and obj.user ==user  or user.is_superuser


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.EMPLOYEE or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.role == User.EMPLOYEE and obj.user == user  or user.is_superuser


class IsObserver(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.OBSERVER or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.role == User.OBSERVER and obj.user == user  or user.is_superuser
    

class StatusChangePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role == User.ADMIN or user.is_superuser


class IsMainEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.MAIN_EMPLOYEE or request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.role == User.MAIN_EMPLOYEE and obj.user == user  or user.is_superuser
    



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
    