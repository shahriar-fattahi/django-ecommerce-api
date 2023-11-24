from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrOwnerOrder(BasePermission):
    """
    Check if Authenticated user is Admin or Owner of the address
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user or request.user.is_admin


class IsAdminOrOwnerOrderItem(BasePermission):
    """
    Check if Authenticated user is Admin or Owner of the address
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.order.user == request.user or request.user.is_admin


class IsOrderIsPending(BasePermission):
    """
    Check if Authenticated user is Admin or Owner of the address
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return not obj.order.paid
