from django.db import models
from django.contrib.auth import get_user_model
from api.core.choices import Roles

User = get_user_model()


class Team(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': Roles.MANAGER},
        related_name='managed_teams'
    )
    members = models.ManyToManyField(
        User,
        related_name='teams',
        limit_choices_to={'role': Roles.USER}
    )

    def __str__(self):
        return self.name