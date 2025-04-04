from django.urls import path
from products import views

urlpatterns = [
    path("/", views.get_products, name="products"),
]
