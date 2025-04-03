# Generated by Django 5.1.7 on 2025-03-21 09:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0005_category_created_at_category_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="brand",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="brand",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="productimage",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="productimage",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
