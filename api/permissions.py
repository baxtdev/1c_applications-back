from rest_framework import permissions

from apps.user.models import User,ADMIN,MAIN_EMPLOYEE,EMPLOYEE,OBSERVER
from apps.utils.utils import get_object_or_none,get_filter_object_or_none



class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role ==  ADMIN or user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.role ==  ADMIN and obj.user ==user  or user.is_superuser


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role ==  EMPLOYEE or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.role ==  EMPLOYEE and obj.user == user  or user.is_superuser


class IsObserver(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role ==  OBSERVER or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.role ==  OBSERVER and obj.user == user  or user.is_superuser
    

class StatusChangePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role ==  ADMIN or user.is_superuser


class IsMainEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role ==  MAIN_EMPLOYEE or request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.role ==  MAIN_EMPLOYEE and obj.user == user  or user.is_superuser
    



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

