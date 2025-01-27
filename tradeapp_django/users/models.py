from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models

from users.managers import CustomUserManager


class User(AbstractUser):
    """
    Represents the custom user model based on AbstractUser
    """

    class RoleChoice(models.TextChoices):
        admin = 'admin'
        analyst = 'analyst'
        user = 'user'

    username = models.CharField(
        max_length=150,
        unique=False,
        blank=True
    )
    email = models.EmailField(
        'E-mail',
        max_length=256,
        unique=True,
        validators=(validate_email,)
    )
    role = models.CharField(
        verbose_name='User role',
        max_length=254,
        choices=RoleChoice.choices,
        blank=False,
        null=False,
        default=RoleChoice.user,
    )
    is_blocked = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('id',)

    def __str__(self):
        return self.email
