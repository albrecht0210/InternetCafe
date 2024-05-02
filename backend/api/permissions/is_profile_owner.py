from rest_framework.permissions import BasePermission

class IsProfileOwner(BasePermission):
    """
    Custom permission to only allow access to the profile owner.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the owner of the profile.
        """
        return obj.id == request.user
