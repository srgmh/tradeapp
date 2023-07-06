from _decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from api_crypto.serializers import (OrderSerializer, SuitcaseSerializer,
                                    WalletSerializer)
from api_crypto.services.assest_service import AssetService
from api_crypto.services.suitcase_service import SuitcaseService
from api_crypto.services.wallet_service import WalletService
from crypto.models import Asset, Suitcase, Wallet


class OrderService:

    @staticmethod
    def create_order(serializer: OrderSerializer,
                     user: get_user_model(),
                     operation_type: str,
                     asset: int,
                     quantity: Decimal):

        serializer.is_valid(raise_exception=True)

        asset = AssetService.get_asset(asset)
        suitcase = SuitcaseService.get_suitcase(user)
        wallet = WalletService.get_wallet(asset, suitcase)

        operation_type_handlers = {
            'sell': OrderService._sell_asset,
            'buy': OrderService._buy_asset,
        }
        operation = operation_type_handlers.get(operation_type)

        if operation:
            return operation(
                user,
                serializer,
                suitcase,
                wallet,
                asset,
                quantity,
            )
        else:
            raise ValidationError("Invalid operation type.")

    @staticmethod
    def _sell_asset(
            user: get_user_model(),
            serializer: OrderSerializer,
            suitcase: Suitcase,
            wallet: Wallet,
            asset: Asset,
            quantity: Decimal,
    ):

        if wallet.balance < quantity:
            raise ValidationError('Not enough asset quantity on wallet!')

        required_amount = asset.price * quantity

        suitcase.balance += required_amount
        suitcase.save()

        wallet.balance -= quantity
        wallet.save()

        order = serializer.save(user=user, is_completed=True)

        response_data = OrderService._create_response(order, wallet, suitcase)

        return response_data

    @staticmethod
    def _buy_asset(
            user: get_user_model(),
            serializer: OrderSerializer,
            suitcase: Suitcase,
            wallet: Wallet,
            asset: Asset,
            quantity: Decimal,
    ):

        required_amount = asset.price * quantity

        if suitcase.balance < required_amount:
            raise ValidationError('Not enough balance on suitcase!')

        suitcase.balance -= required_amount
        suitcase.save()

        wallet.balance += quantity
        wallet.save()

        order = serializer.save(user=user, is_completed=True)

        response_data = OrderService._create_response(order, wallet, suitcase)

        return response_data

    @staticmethod
    def _create_response(order, wallet, suitcase):
        order_serializer = OrderSerializer(order)
        wallet_serializer = WalletSerializer(wallet)
        suitcase_serializer = SuitcaseSerializer(suitcase)

        return {
            'order': order_serializer.data,
            'wallet': wallet_serializer.data,
            'suitcase': suitcase_serializer.data,
        }
