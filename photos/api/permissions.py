"""
Any custom permissions for the photos api
"""
from rest_framework import permissions


class IsAuthenticatedOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return obj.owner == request.user
