from django.db import models
from django.contrib.auth import get_user_model
from . import utils


class Checkout(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order = models.OneToOneField(
        "orders.Order", on_delete=models.SET_NULL, null=True, related_name="checkout"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.order.id}"


class Payment(models.Model):
    ZARINPAL = "z"
    IDPAY = "i"
    PAYMENT_METHOD_CHOICES = ((ZARINPAL, "zarinpal"), (IDPAY, "idpay"))

    FAILED = "f"
    SUCCESS = "s"
    PAYMENT_STATUS_CHOICES = ((FAILED, "failed"), (SUCCESS, "success"))

    checkout = models.ForeignKey(
        Checkout, on_delete=models.CASCADE, related_name="payments"
    )
    method = models.CharField(max_length=1, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(
        max_length=10,
        blank=True,
        editable=False,
        unique=True,
        default=utils.create_new_ref_number,
    )
    status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default="f")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.checkout.user.email} - {self.checkout.id}"
