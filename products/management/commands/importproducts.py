import traceback
from pprint import pprint

import requests
from django.core.management import BaseCommand, CommandError
from django.db import transaction

from products.models import Category, Brand, AvailabilityStatus, Product, ProductImage

CATEGORY_API_URL = "https://dummyjson.com/products/categories"
PRODUCTS_API_URL = "https://dummyjson.com/products"
TOTAL_PRODUCTS = 25


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "limit",
            type=int,
            nargs="?",
            default=10,
            help="Import {limit} products at a time",
        )

    def import_categories(self):
        try:
            res = requests.get(CATEGORY_API_URL)
            categories = res.json()
            with transaction.atomic():
                existing_categories = [category.category_slug for category in
                                       Category.objects.filter(category_slug__in=[c["slug"] for c in categories])]
                pprint(existing_categories)
                Category.objects.bulk_create(
                    [Category(category_slug=category["slug"], category_name=category["name"]) for category in categories
                     if category["slug"] not in existing_categories])
            self.stdout.write(self.style.SUCCESS('Successfully imported categories'))
        except Exception as e:
            print(e)
            # TODO: Handle proper exception
            self.stdout.write(self.style.ERROR('Error in importing categories'))

    def import_brands(self, brands):
        try:
            with transaction.atomic():
                existing_brands = [brand.brand_name for brand in
                                   Brand.objects.filter(brand_name__in=[b for b in brands])]
                pprint(existing_brands)
                Brand.objects.bulk_create([Brand(brand_name=brand) for brand in brands if brand not in existing_brands])
            self.stdout.write(self.style.SUCCESS('Successfully imported brands'))
        except Exception as e:
            print(e)
            # TODO: Handle proper exception
            self.stdout.write(self.style.ERROR('Error in importing brands'))

    def import_availability_statuses(self, statuses):
        try:
            with transaction.atomic():
                existing_statuses = [status.status_name for status in
                                     AvailabilityStatus.objects.filter(
                                         status_name__in=[status_name for status_name in statuses])]
                pprint(existing_statuses)
                AvailabilityStatus.objects.bulk_create(
                    [AvailabilityStatus(status_name=status_name) for status_name in statuses if
                     status_name not in existing_statuses])
            self.stdout.write(self.style.SUCCESS('Successfully imported availability statuses'))
        except Exception as e:
            print(e)
            # TODO: Handle proper exception
            self.stdout.write(self.style.ERROR('Error in importing brands'))

    def import_products(self, products):
        pprint(products)
        try:
            product_images = {}
            products_to_import = []
            with transaction.atomic():
                existing_products = [p.sku for p in Product.objects.filter(sku__in=[p["sku"] for p in products])]
                for product in products:
                    if product["sku"] not in existing_products:
                        product_images[product["sku"]] = product.pop("product_images")
                        products_to_import.append(Product(**product))
                print("product_images")
                pprint(product_images)
                pprint(products_to_import)

                if len(products_to_import) > 0:
                    Product.objects.bulk_create(products_to_import)
                    created_products = Product.objects.filter(sku__in=[p["sku"] for p in products])
                    pprint(created_products)
                    product_images_instances = []
                    for created_product in created_products:
                        product_images_instances.extend(
                            [ProductImage(product=created_product, **product_image) for product_image in
                             product_images[created_product.sku]])
                    ProductImage.objects.bulk_create(product_images_instances)
            self.stdout.write(self.style.SUCCESS('Successfully imported products and product images'))
        except Exception as e:
            print(e)
            # TODO: Handle proper exception
            self.stdout.write(self.style.ERROR('Error in importing products and product images'))

    def handle(self, *args, **options):
        limit = options["limit"]
        skip = 0

        try:
            # Import all categories
            self.import_categories()

            while skip < TOTAL_PRODUCTS - limit:
                # Fetch products
                res = requests.get(f"{PRODUCTS_API_URL}?limit={limit}&skip={skip}")
                res = res.json()
                products = res["products"]

                availability_statuses = set([product["availabilityStatus"] for product in products])
                self.import_availability_statuses(availability_statuses)

                brands = set([product["brand"] for product in products])
                self.import_brands(brands)

                categories = set([product["category"] for product in products])

                products_to_import = []
                imported_categories = {category.category_slug: category for category in
                                       Category.objects.filter(category_slug__in=categories)}
                imported_statuses = {status.status_name: status for status in
                                     AvailabilityStatus.objects.filter(status_name__in=availability_statuses)}
                imported_brands = {brand.brand_name: brand for brand in Brand.objects.filter(brand_name__in=brands)}

                for product in products:
                    product_to_import = {
                        "title": product["title"],
                        "description": product["description"],
                        "category": imported_categories[product["category"]],
                        "discount_percentage": float(product["discountPercentage"]),
                        "price": float(product["price"]),
                        "stock": int(product["stock"]),
                        "brand": imported_brands[product["brand"]],
                        "sku": product["sku"],
                        "availability_status": imported_statuses[product["availabilityStatus"]],
                    }

                    product_images = [{
                        "image_path": product["thumbnail"],
                        "is_thumbnail": True
                    }]
                    if len(product["images"]) > 0:
                        for image_path in product["images"]:
                            product_images.append({
                                "image_path": image_path,
                                "is_thumbnail": False
                            })
                    product_to_import["product_images"] = product_images

                    products_to_import.append(product_to_import)

                self.import_products(products_to_import)

                skip += limit

        except Exception as e:
            print("The error is: ", e)
            traceback.print_exc()  # This prints the full stack trace
            raise CommandError("Error in custom command")

        self.stdout.write(self.style.SUCCESS('Successfully imported'))
