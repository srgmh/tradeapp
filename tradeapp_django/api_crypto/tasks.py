from celery import shared_task

from django_celery_beat.models import PeriodicTask

from api_crypto.services.postponedorder_service import PostponedOrderService
from crypto.models import PostponedOrder


@shared_task
def check_asset_price(postponed_order_id: int) -> str:
    postponed_order = PostponedOrder.objects.get(id=postponed_order_id)
    if postponed_order.in_progress is False:
        task = PeriodicTask.objects.get(id=postponed_order.task_id)
        task.delete()
        return 'Postponed order is not in progress'

    result = PostponedOrderService.create_postponed_order(postponed_order)
    return result
