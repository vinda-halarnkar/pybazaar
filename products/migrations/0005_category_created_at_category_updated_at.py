# Generated by Django 5.1.7 on 2025-03-21 09:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_rename_category_key_category_category_slug_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="category",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
