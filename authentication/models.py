from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        """
        Override the default save method to ensure that the username is set to the
        email address since it's not provided.

        This is done for users who sign up using their email address and do not
        provide a username.
        """
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
