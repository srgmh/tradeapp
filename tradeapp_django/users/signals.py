from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from crypto.models import Suitcase

User = get_user_model()


@receiver(post_save, sender=User)
def create_suitcase(sender, instance, created, **kwargs):
    if created:
        Suitcase.objects.create(user=instance, balance=1000)
