from rest_framework import serializers

from api_users.serializers import UserSerializer
from crypto.models import Asset, Suitcase, Wallet


class AssetSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Asset
        fields = ('id', 'abbreviation', 'price', 'type', 'users', )


class WalletSerializer(serializers.ModelSerializer):

    asset = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ('asset', 'balance', )

    @staticmethod
    def get_asset(obj):
        asset = obj.asset
        return {
            'id': asset.id,
            'abbreviation': asset.abbreviation,
            'type': asset.type,
        }


class SuitcaseSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    wallets = serializers.SerializerMethodField()

    class Meta:
        model = Suitcase
        fields = ('user', 'balance', 'wallets')

    @staticmethod
    def get_wallets(obj):
        wallets = obj.wallets.all()
        wallet_serializer = WalletSerializer(wallets, many=True)
        return wallet_serializer.data
