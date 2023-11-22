from rest_framework import permissions, viewsets
from . import models
from . import serializers

class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD products
    """

    queryset = models.Product.objects.all()

    def get_serializer_class(self):
        # if self.action in ("create", "update", "partial_update", "destroy"):
        #     return ProductWriteSerializer

        # return ProductReadSerializer
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsSellerOrAdmin,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        product = models.Product.objects.filter(id=kwargs.get("pk"))
        if product.exists():
            product.update(views=F("views") + 1)
        return super().retrieve(request, *args, **kwargs)
