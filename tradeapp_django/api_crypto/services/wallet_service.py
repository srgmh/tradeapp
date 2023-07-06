from rest_framework.exceptions import ValidationError

from crypto.models import Asset, Suitcase, Wallet


class WalletService:

    @staticmethod
    def get_wallet(asset: Asset, suitcase: Suitcase) -> Wallet:
        try:
            return Wallet.objects.get(asset=asset, suitcase=suitcase)
        except Wallet.DoesNotExist:
            raise ValidationError('Wallet not found')
