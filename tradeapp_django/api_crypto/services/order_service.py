from typing import Dict

from _decimal import Decimal
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from crypto.models import Asset, Order, Suitcase, Wallet


class OrderService:

    @staticmethod
    def create_order(
            user: get_user_model(),
            order: Order,
            operation_type: str,
            asset: Asset,
            quantity: Decimal
    ) -> Dict[str, bool]:
        suitcase = get_object_or_404(Suitcase, user=user)
        wallet = get_object_or_404(Wallet, suitcase=suitcase, asset=asset)
        suitcase_exchanging_amount = quantity * asset.price
        if operation_type == 'sell':
            result = OrderService._sell_asset(
                order, suitcase, wallet, quantity, suitcase_exchanging_amount
            )
        elif operation_type == 'buy':
            result = OrderService._buy_asset(
                order, suitcase, wallet, quantity, suitcase_exchanging_amount
            )
        else:
            raise ValidationError("Invalid operation type.")

        return result

    @staticmethod
    @atomic
    def _sell_asset(
            order: Order,
            suitcase: Suitcase,
            wallet: Wallet,
            quantity: Decimal,
            suitcase_exchanging_amount: Decimal
    ) -> Dict[str, bool]:
        if wallet.balance < quantity:
            raise ValidationError('Not enough asset quantity on wallet!')
        suitcase.balance += suitcase_exchanging_amount
        wallet.balance -= quantity
        suitcase.save()
        wallet.save()
        OrderService._set_order_status(order, True)

        return {'success': True}

    @staticmethod
    @atomic
    def _buy_asset(
            order: Order,
            suitcase: Suitcase,
            wallet: Wallet,
            quantity: Decimal,
            suitcase_exchanging_amount: Decimal
    ) -> Dict[str, bool]:
        if suitcase.balance < suitcase_exchanging_amount:
            raise ValidationError('Not enough balance on suitcase!')
        suitcase.balance -= suitcase_exchanging_amount
        wallet.balance += quantity
        suitcase.save()
        wallet.save()
        OrderService._set_order_status(order, True)

        return {'success': True}

    @staticmethod
    def _set_order_status(order: Order, status: bool) -> None:
        order.is_completed = status
        order.save()
