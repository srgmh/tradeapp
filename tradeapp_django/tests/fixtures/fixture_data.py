import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from crypto.models import Asset, Order, Wallet

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email='testemail@uu.uu',
        password='testpassword'
    )


@pytest.fixture
def asset():
    return Asset.objects.create(
        abbreviation='ASSET1',
        price='10',
        type='coin'
    )


@pytest.fixture
def subscribed_asset(user):
    asset = Asset.objects.create(
        abbreviation='ASSET2',
        price='10',
        type='coin'
    )
    asset.users.add(user)
    return asset


@pytest.fixture
def subscribed_asset_2(user):
    asset = Asset.objects.create(
        abbreviation='ASSET3',
        price='10',
        type='coin'
    )
    asset.users.add(user)
    return asset


@pytest.fixture
def wallet_100_on_balance(user, subscribed_asset):
    wallet = Wallet.objects.get(suitcase=user.suitcase, asset=subscribed_asset)
    wallet.balance = 100
    wallet.save()
    return wallet


@pytest.fixture
def suitcase_100_on_balance(user):
    suitcase = user.suitcase
    suitcase.balance = 100
    suitcase.save()
    return suitcase


@pytest.fixture
def suitcase_0_on_balance(user):
    suitcase = user.suitcase
    suitcase.balance = 0
    suitcase.save()
    return suitcase
