from django.db import models


class Category(models.Model):
    class Meta:
        orderinf = "-id"

    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    is_subcategory = models.BooleanField(default=False)
    subcategory = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    class Meta:
        ordering = ["-id"]

    VARIANT = (
        ("None", "none"),
        ("Size", "size"),
        ("Color", "color"),
        ("Both", "both"),
    )
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=VARIANT)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    color = models.ForeignKey("Color", on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey("Size", on_delete=models.CASCADE, blank=True, null=True)

    @property
    def final_price(self):
        return int(self.unit_price - (self.unit_price * self.discount / 100))


class ProductGallery(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="media/products")


class Size(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    hex = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
