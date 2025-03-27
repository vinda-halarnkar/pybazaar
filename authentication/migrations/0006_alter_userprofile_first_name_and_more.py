# Generated by Django 5.1.7 on 2025-03-27 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0005_userprofile_groups_userprofile_user_permissions_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="first_name",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="is_superuser",
            field=models.BooleanField(
                default=False,
                help_text="Designates that this user has all permissions without explicitly assigning them.",
                verbose_name="superuser status",
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="last_name",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
