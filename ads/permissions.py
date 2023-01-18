from rest_framework import permissions

from users.models import User


class IsOwner(permissions.BasePermission):
    message = 'You are not an owner.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsModerator(permissions.BasePermission):
    message = "You are not a moderator"

    def has_permission(self, request, view):
        return request.user.role == User.MODERATOR
