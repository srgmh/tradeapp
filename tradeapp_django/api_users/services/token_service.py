from django.conf import settings
from django.contrib.auth import get_user_model

from api_users.utils import generate_token

SECRET_KEY = settings.JWT_SECRET_KEY
User = get_user_model()


class TokenService:

    @staticmethod
    def generate_jwt_token(user_id: int, minutes: int) -> str:
        """
        Generate access and refresh JWT tokens by user_id
        and token expiration time from settings.
        """

        token = generate_token(user_id, minutes)

        return token
