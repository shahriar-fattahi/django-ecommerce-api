from rest_framework import serializers
from . import models


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ("name",)


class CategoryReadOnlySerializer(serializers.ModelSerializer):
    parent = ParentCategorySerializer()

    class Meta:
        model = models.Category
        exclude = ("modified_date",)

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Color
        fields = "__all__"


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Size
        fields = "__all__"


class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductGallery
        fields = "__all__"


class ProductReadOnlySerializer(serializers.ModelSerializer):
    seller = serializers.CharField(source="seller.email")
    categories = serializers.SerializerMethodField()
    colors = ColorSerializer(many=True)
    brand = BrandSerializer()
    sizes = SizeSerializer(many=True)
    images = serializers.SerializerMethodField()
    final_price = serializers.IntegerField()

    class Meta:
        model = models.Product
        exclude = ("updated_date", "views")

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields

    def get_categories(self, obj):
        data = []
        for _category in obj.categories.all():
            category = CategoryReadOnlySerializer(_category)
            data.append(category.data)
        return data

    def get_images(sef, obj):
        data = []
        for _image in obj.images.all():
            image = ProductGallerySerializer(_image)
            data.append(image.data)
        return data


class ProductWriteOnlySerializer(serializers.ModelSerializer):
    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())
    uploaded_images = serializers.ListField(
        child=serializers.FileField(
            max_length=1000000, allow_empty_file=False, use_url=False
        ),
        required=True,
    )

    def validate(self, attrs):
        status = attrs.get("status")
        if status:
            if status in ("Color", "Both"):
                if not attrs.get("colors"):
                    raise serializers.ValidationError("colors field is required.")
            if status in ("Size", "Both"):
                if not attrs.get("sizes"):
                    raise serializers.ValidationError("sizes field is required.")
        return super().validate(attrs)

    class Meta:
        model = models.Product
        exclude = ("created_date", "updated_date", "views")

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.write_only = True
        return fields

    def create(self, validated_data):
        uploaded_data = validated_data.pop("uploaded_images")
        categories = validated_data.pop("categories")
        colors = validated_data.pop("colors")
        sizes = validated_data.pop("sizes")
        obj = self.Meta.model.objects.create(**validated_data)
        for category in categories:
            obj.categories.add(category)
        for color in colors:
            obj.colors.add(color)
        for size in sizes:
            obj.sizes.add(size)
        obj.save()
        for uploaded_item in uploaded_data:
            models.ProductGallery.objects.create(product=obj, image=uploaded_item)
        return obj
