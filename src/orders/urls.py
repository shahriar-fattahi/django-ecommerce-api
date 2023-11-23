from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "orders"

router = DefaultRouter()
router.register(r"^(?P<order_id>\d+)/order-items", views.OrderItemViewSet)
router.register(r"", views.OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
