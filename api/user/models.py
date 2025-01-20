from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from api.core.choices import Roles
# Create your models here.


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", Roles.ADMIN)

        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.USER
    )
    email = models.EmailField(unique=True)
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"

