import traceback

import requests
from django.core.management import BaseCommand, CommandError
from django.db import transaction, DatabaseError

from products.models import Category, Brand, AvailabilityStatus, Product, ProductImage

CATEGORY_API_URL = "https://dummyjson.com/products/categories"
PRODUCTS_API_URL = "https://dummyjson.com/products"
TOTAL_PRODUCTS = 200


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "limit",
            type=int,
            nargs="?",
            default=10,
            help="Import {limit} products at a time",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        skip = 0

        try:
            # Import all categories
            self.import_categories()

            batch = 1
            while skip < TOTAL_PRODUCTS:
                self.log_info(f"Importing batch {batch}")

                # Fetch products
                res = requests.get(f"{PRODUCTS_API_URL}?limit={limit}&skip={skip}")
                res.raise_for_status()
                products = res.json()["products"]

                availability_statuses = set(product["availabilityStatus"] for product in products)
                self.import_availability_statuses(availability_statuses)

                brands = set(product["brand"] for product in products if "brand" in product)
                self.import_brands(brands)

                categories = set(product["category"] for product in products)
                imported_categories = {category.category_slug: category for category in
                                       Category.objects.filter(category_slug__in=categories)}
                imported_statuses = {status.status_name: status for status in
                                     AvailabilityStatus.objects.filter(status_name__in=availability_statuses)}
                imported_brands = {brand.brand_name: brand for brand in Brand.objects.filter(brand_name__in=brands)}

                products_to_import = []
                for product in products:
                    product_to_import = {
                        "title": product["title"],
                        "description": product["description"],
                        "category": imported_categories[product["category"]],
                        "discount_percentage": float(product["discountPercentage"]),
                        "price": float(product["price"]),
                        "stock": int(product["stock"]),
                        "sku": product["sku"],
                        "availability_status": imported_statuses[product["availabilityStatus"]],
                    }

                    if "brand" in product:
                        product_to_import["brand"] = imported_brands[product["brand"]]

                    product_images = [{
                        "image_path": product["thumbnail"],
                        "is_thumbnail": True
                    }]
                    if product["images"]:
                        for image_path in product["images"]:
                            product_images.append({
                                "image_path": image_path,
                                "is_thumbnail": False
                            })
                    product_to_import["product_images"] = product_images

                    products_to_import.append(product_to_import)

                self.import_products(products_to_import)

                skip += limit
                batch += 1

        except Exception as e:
            self.log_error(e)
            raise CommandError("Error in custom command")

        self.log_success('Successfully imported')

    def import_categories(self):
        try:
            response = requests.get(CATEGORY_API_URL)
            response.raise_for_status()
            categories = response.json()

            category_slugs = [category["slug"] for category in categories]
            existing_categories = set(Category.objects.filter(category_slug__in=category_slugs)
                                      .values_list('category_slug', flat=True))

            new_categories = [
                Category(category_slug=category["slug"], category_name=category["name"])
                for category in categories
                if category["slug"] not in existing_categories
            ]

            if new_categories:
                with transaction.atomic():
                    Category.objects.bulk_create(new_categories)
                self.log_success('Successfully imported categories.')
            else:
                self.log_success('No new categories to import.')

        except requests.RequestException as e:
            self.log_error(f'Request error in importing categories: {e}')
        except DatabaseError as e:
            self.log_error(f'Database error in importing categories: {e}')
        except Exception as e:
            self.log_error(f'Error in importing categories: {e}')

    def import_brands(self, brands):
        try:
            with transaction.atomic():
                existing_brands = set(Brand.objects.filter(brand_name__in=brands).values_list('brand_name', flat=True))
                new_brands = [Brand(brand_name=brand) for brand in brands if brand not in existing_brands]

                if new_brands:
                    Brand.objects.bulk_create(new_brands)
                    self.log_success('Successfully imported brands')
                else:
                    self.log_success('No new brands to import')

        except DatabaseError as e:
            self.log_error(f'Database error in importing brands: {e}')
        except Exception as e:
            self.log_error(f'Error in importing brands: {e}')

    def import_availability_statuses(self, statuses):
        try:
            with transaction.atomic():
                existing_statuses = AvailabilityStatus.objects.filter(status_name__in=statuses).values_list(
                    'status_name', flat=True)

                new_statuses = [
                    AvailabilityStatus(status_name=status_name)
                    for status_name in statuses
                    if status_name not in existing_statuses
                ]

                if new_statuses:
                    AvailabilityStatus.objects.bulk_create(new_statuses)
                    self.log_success('Successfully imported availability statuses.')
                else:
                    self.log_success('No new availability statuses to import.')
        except DatabaseError as e:
            self.log_error(f'Database error in importing availability statuses: {e}')
        except Exception as e:
            self.log_error(f'Error in importing availability statuses: {e}')

    def import_products(self, products):
        try:
            product_images = {}
            products_to_import = []

            with transaction.atomic():
                existing_products = Product.objects.filter(
                    sku__in=[product["sku"] for product in products]).values_list('sku', flat=True)

                for product in products:
                    if product["sku"] not in existing_products:
                        product_images[product["sku"]] = product.pop("product_images")
                        products_to_import.append(Product(**product))

                if products_to_import:
                    skus_to_import = [product.sku for product in products_to_import]
                    self.log_info(f"Importing products with SKUs: {skus_to_import}")

                    with transaction.atomic():
                        Product.objects.bulk_create(products_to_import)
                        self.log_success('Successfully imported products.')

                        created_products = Product.objects.filter(sku__in=skus_to_import)

                        product_images_instances = []
                        for created_product in created_products:
                            product_images_instances.extend(
                                [ProductImage(product=created_product, **image) for image in
                                 product_images[created_product.sku]]
                            )
                            ProductImage.objects.bulk_create(product_images_instances)
                            self.log_success(
                                f'Successfully imported product images for product SKU: "{created_product.sku}".')
                else:
                    self.log_success('No new products to import.')
        except DatabaseError as e:
            self.log_error(f'Database error in importing products and product images: {e}')
        except Exception as e:
            self.log_error(f'Error in importing products and product images: {e}')

    def log_error(self, msg):
        self.stderr.write(self.style.ERROR(msg))
        traceback.print_exc(file=self.stderr)

    def log_success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def log_info(self, msg):
        self.stdout.write(self.style.NOTICE(msg))
