
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from api.core.choices import Roles

User = get_user_model()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Roles.ADMIN

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Roles.MANAGER

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Roles.USER
