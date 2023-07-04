from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from crypto.models import Asset, Suitcase, Wallet

User = get_user_model()


@receiver(m2m_changed, sender=Asset.users.through)
def create_wallet(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    Create wallet with asset, in which User has subscribed.
    """

    if action == "post_add":
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            suitcase = Suitcase.objects.get(user=user)
            wallet, created = Wallet.objects.get_or_create(
                suitcase=suitcase, asset=instance)
            if created:
                wallet.balance = 0
                wallet.save()
