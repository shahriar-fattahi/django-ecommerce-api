from rest_framework import serializers
from . import models


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = "__all__"


class TransactionsReadSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()

    class Meta:
        model = models.Checkout
        fields = ["id", "order", "is_completed", "payments"]

    def get_payments(self, obj):
        data = []
        for _item in obj.payments.all():
            item = PaymentSerializer(_item)
            data.append(item.data)
        return data
