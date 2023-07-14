import pytest
from rest_framework.reverse import reverse

from crypto.models import PostponedOrder


@pytest.mark.django_db
def test_create_postponed_order(api_client, user, subscribed_asset):
    api_client.force_authenticate(user=user)
    url = reverse('postponed_orders-create-postponed-order')
    data = {
        'operation_type': 'sell',
        'quantity': 100500,
        'asset': subscribed_asset.id,
        'price': 15,
        'price_way': 'above',
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    assert response.data['Postponed order created!'] is True
    assert PostponedOrder.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_create_postponed_order_not_subscribed_asset(api_client, user, asset):
    api_client.force_authenticate(user=user)
    url = reverse('postponed_orders-create-postponed-order')
    data = {
        'operation_type': 'sell',
        'quantity': 100500,
        'asset': asset.id,
        'price': 15,
        'price_way': 'above',
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 400
    assert not PostponedOrder.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_create_postponed_order_task_created(api_client, user, subscribed_asset):
    api_client.force_authenticate(user=user)
    url = reverse('postponed_orders-create-postponed-order')
    data = {
        'operation_type': 'sell',
        'quantity': 100500,
        'asset': subscribed_asset.id,
        'price': 11600,
        'price_way': 'above',
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    assert response.data['Postponed order created!'] is True
    assert PostponedOrder.objects.filter(user=user).exists()
    postponed_order = PostponedOrder.objects.get(user=user)
    assert postponed_order.task_id is not None


@pytest.mark.django_db
def test_create_postponed_order_unauthenticated(
        api_client,
        user,
        subscribed_asset
):
    url = reverse('postponed_orders-create-postponed-order')
    data = {
        'asset': subscribed_asset.id,
        'price': 15,
        'price_way': 'above',
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 403
    assert not PostponedOrder.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_create_postponed_order_missing_fields(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('postponed_orders-create-postponed-order')
    data = {}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 400
    assert 'operation_type' in response.data
    assert 'quantity' in response.data
    assert 'asset' in response.data
    assert 'price' in response.data
    assert 'price_way' in response.data
    assert not PostponedOrder.objects.filter(user=user).exists()
