from rest_framework.permissions import BasePermission


class IsCheckOut(BasePermission):
    """
    Check if Authenticated user is Admin or Owner of the address
    """

    def has_permission(self, request, view):
        if request.session.get("order_pay"):
            return True
        return False
