from rest_framework import viewsets, permissions
from . import models
from users import authentication
from . import serializers
from .permissions import IsAdminOrOwnerOrder, IsAdminOrOwnerOrderItem, IsOrderIsPending


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    CRUD order items
    """

    authentication_classes = (authentication.CustomUserAuthentication,)
    serializer_class = serializers.OrderItemSerializer
    queryset = models.OrderItem.objects.all()
    permission_classes = (IsAdminOrOwnerOrderItem,)

    def get_queryset(self):
        order_id = self.kwargs.get("order_id")
        return self.queryset.filter(order__id=order_id)

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            self.permission_classes += (IsOrderIsPending,)
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    """
    CRUD orders
    """

    authentication_classes = (authentication.CustomUserAuthentication,)
    queryset = models.Order.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return serializers.OrderWriteOnlySerializer
        return serializers.OrderReadOnlySerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return self.queryset
        return self.queryset.filter(user_id=self.request.user.id)

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        else:
            self.permission_classes = (IsAdminOrOwnerOrder,)

        return super().get_permissions()
