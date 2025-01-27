import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_user_wallets(
        api_client,
        user,
        subscribed_asset,
        subscribed_asset_2,
        asset
):
    url = reverse('wallets-list')
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
