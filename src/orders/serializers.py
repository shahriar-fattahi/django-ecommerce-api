from rest_framework import serializers
from . import models
from products.models import Product
import datetime
from django.conf import settings
from pytz import timezone


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    price = serializers.IntegerField(source="product.final_price", read_only=True)
    total_cost = serializers.IntegerField(source="get_cost", read_only=True)

    class Meta:
        model = models.OrderItem
        fields = "__all__"
        read_only_fields = ("order",)

    def create(self, validated_data):
        order_id = self.context["view"].kwargs.get("order_id")
        try:
            order = models.Order.objects.get(id=order_id, paid=False)
        except models.Order.DoesNotExist:
            raise serializers.ValidationError("Order Does not exist")
        product = validated_data["product"]
        for item in order.items.all():
            if item.product.id == product.id:
                item.quantity += validated_data["quantity"]
                item.save()
                return item
        return self.Meta.model.objects.create(order=order, **validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class OrderReadOnlySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    get_total_price = serializers.IntegerField()

    class Meta:
        model = models.Order
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields

    def get_items(self, obj):
        data = []
        for _item in obj.items.all():
            item = OrderItemSerializer(_item)
            data.append(item.data)
        return data


class OrderWriteOnlySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    coupon = serializers.CharField(required=False)

    class Meta:
        model = models.Order
        exclude = ("created", "updated", "discount")

    def validate(self, attrs):
        code = attrs.get("coupon")
        time = datetime.datetime.now(timezone(settings.TIME_ZONE))
        if code:
            try:
                coupon = models.Coupon.objects.get(
                    code__iexact=code,
                    valid_from__lte=time,
                    valid_to__gte=time,
                    active=True,
                )
            except models.Coupon.DoesNotExist:
                raise serializers.ValidationError("Coupon is invalid")
        return attrs

    def create(self, validated_data):
        coupon = validated_data.pop("coupon") if "coupon" in validated_data else None
        obj = self.Meta.model.objects.create(**validated_data)
        if coupon:
            obj.discount = models.Coupon.objects.get(code__iexact=coupon).discount
        obj.save()
        return obj

    def update(self, instance, validated_data):
        validated_data.pop("user")
        return super().update(instance, validated_data)
