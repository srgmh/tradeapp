from celery import shared_task
from datetime import datetime

from api_crypto.services.postponedorder_service import PostponedOrderService
from crypto.models import Asset, PostponedOrder


@shared_task
def process_postponed_orders() -> str:
    postponed_orders = PostponedOrder.objects.filter(in_progress=True)

    for postponed_order in postponed_orders:
        check_asset_price.delay(postponed_order.id)

    return 'Postponed orders processing initiated at {}'.format(datetime.now())


@shared_task
def check_asset_price(postponed_order_id: int) -> str:
    postponed_order = PostponedOrder.objects.get(id=postponed_order_id)
    result = PostponedOrderService.create_postponed_order(postponed_order)

    return result
