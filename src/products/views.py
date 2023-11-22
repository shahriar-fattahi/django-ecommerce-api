from rest_framework import permissions, viewsets
from . import models
from . import serializers
from django.db.models import F
from users.authentication import CustomUserAuthentication
from . import permissions as myCustomPermission


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD products
    """

    authentication_classes = (CustomUserAuthentication,)
    queryset = models.Product.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return serializers.ProductWriteOnlySerializer
        return serializers.ProductReadOnlySerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (myCustomPermission.IsAdminOrSeller,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        product = models.Product.objects.filter(id=kwargs.get("pk"))
        if product.exists():
            product.update(views=F("views") + 1)
        return super().retrieve(request, *args, **kwargs)
