import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from crypto.models import Suitcase, Wallet

User = get_user_model()


@pytest.mark.django_db
def test_asset_list(api_client, asset, user):
    url = reverse('assets-list')
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['abbreviation'] == asset.abbreviation


@pytest.mark.django_db
def test_asset_detail(api_client, asset, user):
    url = reverse('assets-detail', args=[asset.id])
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json()['abbreviation'] == asset.abbreviation


@pytest.mark.django_db
def test_asset_subscribe(api_client, asset, user):
    url = reverse('assets-subscribe')
    data = {'asset_id': asset.id}
    api_client.force_authenticate(user=user)
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.json()['success'] is True
    assert response.json()['message'] == 'Subscribed successfully.'
    assert asset.users.filter(id=user.id).exists()
    assert Wallet.objects.filter(
        suitcase=user.suitcase,
        asset=asset,
    ).exists() is True


@pytest.mark.django_db
def test_asset_subscribe_already_subscribed(api_client, subscribed_asset, user):
    url = reverse('assets-subscribe')
    data = {'asset_id': subscribed_asset.id}
    api_client.force_authenticate(user=user)
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.json()['success'] is True
    assert response.json()['message'] == 'You are already subscribed to this asset'


@pytest.mark.django_db
def test_asset_unsubscribe(api_client, subscribed_asset, user):
    url = reverse('assets-unsubscribe')
    data = {'asset_id': subscribed_asset.id}
    api_client.force_authenticate(user=user)
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.json()['success'] is True
    assert response.json()['message'] == 'Unsubscribed successfully.'
    assert not subscribed_asset.users.filter(id=user.id).exists()


@pytest.mark.django_db
def test_asset_unsubscribe_not_subscribed(api_client, asset, user):
    url = reverse('assets-unsubscribe')
    data = {'asset_id': asset.id}
    api_client.force_authenticate(user=user)
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.json()['success'] is True
    assert response.json()['message'] == 'You are not subscribed to this asset.'