from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the owner of the object.
        """
        # Assuming your object has an owner field, replace it with the appropriate field name
        return obj.owner == request.user
    