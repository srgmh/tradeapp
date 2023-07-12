import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from crypto.models import Asset

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
        abbreviation='BTC',
        price='50000.00',
        type='coin'
    )


@pytest.fixture
def subscribed_asset(user):
    asset = Asset.objects.create(
        abbreviation='ETH',
        price='2000.00',
        type='coin'
    )
    asset.users.add(user)
    return asset
