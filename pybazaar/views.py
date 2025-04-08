from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import DatabaseError
from products.models import Category, Product
from django.db.models import Min
import logging

logger = logging.getLogger(__name__)


@login_required
def index(request):
    return render(request, "index.html")


def home(request):
    try:
        products = (
            Product.objects.filter(images__is_thumbnail=False)
            .order_by("-created_at")
            .values("id", "title", "description")
            .annotate(image_path=Min("images__image_path"))[:3]
        )

        categories = Category.objects.values("category_name")[:5]

    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        products = []
        categories = []

    context = {"latest_products": products, "categories": list(categories)}
    return render(request, "home.html", context)


def contact(request):
    return render(request, "contact.html")
