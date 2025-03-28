from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    username = models.CharField(
        max_length=150, unique=True, blank=True, null=True
    )  # Allow blank username

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # Remove username from required fields

    def save(self, *args, **kwargs):
        """
        Override the default save method to ensure that the username is set to the
        email address if it is not provided.

        This is useful for users who sign up using their email address and do not
        provide a username.
        """
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
