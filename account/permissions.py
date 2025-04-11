from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to allow access only to the owner of the object.
    """
    def has_object_permission(self, request, obj):
        return obj.user == request.user