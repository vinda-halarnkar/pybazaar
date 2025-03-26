from django.contrib import admin

from products.models import ProductImage, AvailabilityStatus, Brand, Category, Product

# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(AvailabilityStatus)
admin.site.register(Product)
admin.site.register(ProductImage)
