from . import views
from django.urls import path

app_name = "checkouts"

urlpatterns = [
    path("pay/<int:order_id>/", views.OrderPayView.as_view(), name="order-pay"),
    path("verify/", views.PaymentVerifyView.as_view(), name="payment-verify"),
]
