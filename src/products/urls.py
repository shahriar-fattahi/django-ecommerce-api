from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products import views

app_name = "products"

router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r"", views.ProductViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
