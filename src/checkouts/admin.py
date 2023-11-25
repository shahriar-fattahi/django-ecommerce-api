from django.contrib import admin
from . import models


@admin.register(models.Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "order",
        "created_at",
        "updated_at",
        "is_completed",
    )
    list_filter = ("is_completed", "updated_at", "user")


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "checkout",
        "method",
        "transaction_id",
        "status",
        "get_price",
        "created_at",
    )

    def get_price(self, obj):
        return obj.checkout.order.get_total_price()

    list_filter = ("created_at", "status")
