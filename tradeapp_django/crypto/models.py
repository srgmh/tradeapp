from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Asset(models.Model):
    """Represents a financial asset."""

    class AssetTypeChoice(models.TextChoices):
        coin = 'coin'
        stock = 'stock'

    users = models.ManyToManyField(
        to=User, verbose_name='Users', related_name='assets', blank=True)
    abbreviation = models.CharField(
        verbose_name='Abbreviation', max_length=10, unique=True, )
    price = models.DecimalField(
        verbose_name='Price', max_digits=19, decimal_places=10, )
    type = models.CharField(
        verbose_name='Type', max_length=5,
        choices=AssetTypeChoice.choices, blank=False, null=False, )

    class Meta:
        verbose_name_plural = 'Assets'
        ordering = ('abbreviation', )

    def __str__(self):
        return self.abbreviation


class Suitcase(models.Model):
    """Represents a collection of wallets owned by a user."""

    user = models.OneToOneField(
        to=User, verbose_name='User', on_delete=models.CASCADE, )
    balance = models.DecimalField(
        verbose_name='Balance', max_digits=19, decimal_places=10, )

    class Meta:
        verbose_name_plural = 'Suitcases'
        ordering = ('-user', )

    def __str__(self):
        return f'{self.user} suitcase, balance: {self.balance}'


class Wallet(models.Model):
    """Represents a wallet containing assets."""

    suitcase = models.ForeignKey(
        to=Suitcase, verbose_name='Suitcase',
        related_name='wallets', on_delete=models.CASCADE, )
    asset = models.ForeignKey(
        to=Asset, verbose_name='Asset',
        related_name='wallets', on_delete=models.CASCADE, )
    balance = models.DecimalField(
        verbose_name='Balance', max_digits=19,
        decimal_places=10, default=0, )

    class Meta:
        verbose_name_plural = 'Wallets'

    def __str__(self):
        return f'{self.asset.abbreviation}: {self.balance}'


class Order(models.Model):
    """Represents a financial order placed by a user."""

    class OperationTypeChoice(models.TextChoices):
        sell = 'sell'
        buy = 'buy'

    operation_type = models.CharField(
        verbose_name='Type', max_length=254,
        choices=OperationTypeChoice.choices, blank=False, null=False, )
    user = models.ForeignKey(
        to=User, verbose_name='User', on_delete=models.CASCADE, )
    asset = models.ForeignKey(
        to=Asset, verbose_name='Asset', on_delete=models.CASCADE, )
    quantity = models.DecimalField(
        verbose_name='Quantity', max_digits=19, decimal_places=10, )
    timestamp = models.DateTimeField(
        verbose_name='Timestamp', auto_now_add=True, )
    is_completed = models.BooleanField(
        default=False)

    class Meta:
        verbose_name_plural = 'Orders'
        ordering = ('-timestamp', )

    def __str__(self):
        return (f'{self.user}: '
                f'{self.asset.abbreviation} - {self.quantity}')


class PostponedOrder(Order):
    """Represents a postponed financial order."""

    class PriceWayChoice(models.TextChoices):
        above = 'above'
        below = 'below'

    price = models.DecimalField(
        verbose_name='Price', max_digits=19, decimal_places=10, )
    price_way = models.CharField(
        verbose_name='Price way', max_length=254,
        choices=PriceWayChoice.choices, blank=False, null=False, )
    expiration_date = models.DateTimeField(
        verbose_name='Expiration date', auto_now_add=True,)
    in_progress = models.BooleanField(
        default=True)
    task_id = models.IntegerField(
        verbose_name='Task ID', null=True
    )

    class Meta:
        verbose_name_plural = 'PostponedOrders'
        ordering = ('-timestamp', )

    def __str__(self):
        return (f'{self.user}: '
                f'{self.asset.abbreviation} - {self.quantity}')
