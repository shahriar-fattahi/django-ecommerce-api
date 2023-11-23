from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter


schema_view = get_schema_view(
    openapi.Info(
        title="E-commerce API",
        default_version="1.0.0",
        description="Django Rest Framework E-commerce API",
        contact=openapi.Contact(email="alifattahisf@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("users/", include("users.urls", namespace="users")),
                path("products/", include("products.urls", namespace="products")),
                path("orders/", include("orders.urls", namespace="orders")),
                path(
                    "swagger/schema/",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="schema-swagger",
                ),
            ]
        ),
    ),
]
