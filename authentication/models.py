from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    email = models.EmailField(unique=True, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []