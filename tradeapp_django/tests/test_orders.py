import pytest
from django.urls import reverse

from crypto.models import Order, Wallet, Suitcase


@pytest.mark.django_db
def test_create_sell_order(
        api_client,
        user,
        subscribed_asset,
        wallet_100_on_balance,
        suitcase_100_on_balance
):
    url = reverse('orders-create-order')
    api_client.force_authenticate(user=user)
    data = {
        'operation_type': 'sell',
        'asset': subscribed_asset.id,
        'quantity': 1,
        'user': user.id
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.json()['success'] is True
    assert Wallet.objects.get(asset=subscribed_asset).balance == 100 - 1
    assert Suitcase.objects.get(user=user).balance == 100 + 10
    assert Order.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_create_buy_order(
        api_client,
        user,
        subscribed_asset,
        wallet_100_on_balance,
        suitcase_100_on_balance
):
    url = reverse('orders-create-order')
    api_client.force_authenticate(user=user)
    data = {
        'operation_type': 'buy',
        'asset': subscribed_asset.id,
        'quantity': 1,
        'user': user.id
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.json()['success'] is True
    assert Wallet.objects.get(asset=subscribed_asset).balance == 100 + 1
    assert Suitcase.objects.get(user=user).balance == 100 - 10
    assert Order.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_create_sell_order_not_enough_asset_quantity(
        api_client,
        user,
        subscribed_asset
):
    url = reverse('orders-create-order')
    api_client.force_authenticate(user=user)
    data = {
        'operation_type': 'sell',
        'asset': subscribed_asset.id,
        'quantity': 1000000,
        'user': user.id
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.data['success'] is False
    assert response.data['message'] == 'Not enough asset quantity on wallet!'


@pytest.mark.django_db
def test_create_sell_order_not_enough_wallet_balance(
        api_client,
        user,
        subscribed_asset,
        suitcase_0_on_balance
):
    url = reverse('orders-create-order')
    api_client.force_authenticate(user=user)
    data = {
        'operation_type': 'buy',
        'asset': subscribed_asset.id,
        'quantity': 1,
        'user': user.id
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.data['success'] is False
    assert response.data['message'] == 'Not enough balance on suitcase!'
