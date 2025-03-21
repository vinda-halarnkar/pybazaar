from django.db import models


class Category(models.Model):
    category_slug = models.CharField(max_length=30, unique=True)
    category_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name


class AvailabilityStatus(models.Model):
    status_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.status_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    price = models.FloatField()
    discount_percentage = models.FloatField()
    stock = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='products')
    sku = models.CharField(max_length=20, unique=True)
    availability_status = models.ForeignKey(AvailabilityStatus, on_delete=models.SET_NULL, null=True,
                                            related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sku} - {self.title}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_path = models.CharField(max_length=255, null=False)
    is_thumbnail = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.product.title}"
