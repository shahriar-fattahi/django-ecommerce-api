from django.contrib import admin
from . import models


@admin.register(models.Category)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("name", "is_subcategory", "subcategory", "modified_date")


class ProductGalleryInlines(admin.TabularInline):
    model = models.ProductGallery
    extra = 0


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "unit_price", "discount", "available", "status")
    raw_id_fields = ("category", "color", "size")
    inlines = (ProductGalleryInlines,)


@admin.register(models.ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ("id", "get_product")

    @admin.display(description="Product Name")
    def get_product(self, obj):
        return obj.product.name


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "hex")


@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
