from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models


class User(AbstractUser):
    """
    Represents the custom user model based on AbstractUser
    """

    class RoleChoice(models.TextChoices):
        admin = 'administrator'
        analyst = 'analyst'
        user = 'user'

    email = models.EmailField(
        'E-mail', max_length=256, unique=True, validators=(validate_email,)
    )
    role = models.CharField(
        verbose_name='User role',
        max_length=254,
        choices=RoleChoice.choices,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('id',)

    def __str__(self):
        return self.username
