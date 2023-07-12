import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from crypto.models import Suitcase

User = get_user_model()


@pytest.mark.django_db
def test_registration_user(api_client):
    url = reverse('users-register')
    new_user_data = {
        'email': 'testuser@test.test',
        'password': '12345678'
    }
    response = api_client.post(url, new_user_data)
    user = User.objects.filter(
        email='testuser@test.test',
        role=User.RoleChoice.user,
        is_blocked=False
    ).first()
    assert response.status_code == 200
    assert user is not None
    assert user.suitcase is not None
    assert response.json()['email'] == user.email
    assert response.json()['role'] == User.RoleChoice.user
    assert response.json()['is_blocked'] is False


@pytest.mark.django_db
def test_registration_user_with_email_of_existing_user(api_client, user):
    url = reverse('users-register')
    response = api_client.post(url, data={'email': user.email})
    assert response.json()['email'] == [
        'User with this E-mail already exists.'
    ]


# def test_login_user(api_client, user):
#     url = reverse()