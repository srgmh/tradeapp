from rest_framework import serializers

from api_users.serializers import UserSerializer
from crypto.models import Asset, Order, Suitcase, Wallet, PostponedOrder


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


class OrderSerializer(serializers.ModelSerializer):

    quantity = serializers.DecimalField(max_digits=19, decimal_places=10,
                                        coerce_to_string=False)

    class Meta:
        model = Order
        fields = ('id', 'user', 'operation_type', 'asset',
                  'quantity', 'timestamp', 'is_completed', )
        read_only_fields = ('user', 'timestamp', 'is_completed')


class PostponedOrderSerializer(serializers.ModelSerializer):

    quantity = serializers.DecimalField(max_digits=19, decimal_places=10,
                                        coerce_to_string=False)

    class Meta:
        model = PostponedOrder
        fields = ('id', 'user', 'operation_type', 'asset',
                  'quantity', 'timestamp',
                  'price', 'price_way', 'in_progress', 'is_completed',)
        read_only_fields = ('user', 'timestamp', 'is_completed', 'in_progress')
