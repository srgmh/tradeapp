import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_suitcase(api_client, user):
    url = reverse('suitcases-list')
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == 200
    assert 'wallets' and 'balance' in response.data[0]
