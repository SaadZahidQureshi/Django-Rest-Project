

from django.db import models

class Roles(models.TextChoices):
    ADMIN = "admin", ("Admin")
    MANAGER = "manager", ("Manager")
    USER = "user", ("User")
    