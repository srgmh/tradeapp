from django.db.transaction import atomic
from django.utils import timezone

from api_crypto.services.order_service import OrderService
from crypto.models import PostponedOrder, Order


class PostponedOrderService(OrderService):

    @staticmethod
    def create_postponed_order(postponed_order: PostponedOrder) -> str:
        current_asset_price = postponed_order.asset.price

        if (
            postponed_order.operation_type == Order.OperationTypeChoice.sell
            and postponed_order.price_way == PostponedOrder.PriceWayChoice.above
            and current_asset_price >= postponed_order.price
        ) or (
            postponed_order.operation_type == Order.OperationTypeChoice.buy
            and postponed_order.price_way == PostponedOrder.PriceWayChoice.below
            and current_asset_price <= postponed_order.price
        ):
            return PostponedOrderService._execute_order(postponed_order)

        return f'Order {postponed_order.id} is still in progress'

    @staticmethod
    @atomic
    def _execute_order(postponed_order: PostponedOrder) -> str:
        result = PostponedOrderService.create_order(
            user=postponed_order.user,
            order=postponed_order,
            operation_type=postponed_order.operation_type,
            asset=postponed_order.asset,
            quantity=postponed_order.quantity
        )
        if result['success']:
            PostponedOrderService._set_order_progress(
                postponed_order, False
            )

            return f"Order {postponed_order.id} successfully executed at {timezone.now()}"

        return f'Failed to execute order {postponed_order.id}. {result["message"]}'

    @staticmethod
    def _set_order_progress(
            postponed_order: PostponedOrder,
            progress: bool
    ) -> None:
        postponed_order.in_progress = progress
        postponed_order.save()
