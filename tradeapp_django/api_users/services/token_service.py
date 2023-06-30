from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

SECRET_KEY = settings.JWT_SECRET_KEY
User = get_user_model()


class TokenService:

    @staticmethod
    def generate_token(user_id: int) -> tuple:
        """
        Generate access and refresh JWT tokens by user_id
        and token expiration time from settings.
        """

        def get_expiry_time(minutes: int):
            return datetime.utcnow() + timedelta(minutes=minutes)

        access_token = jwt.encode(
            payload={
                'user_id': user_id,
                'exp': get_expiry_time(
                    settings.ACCESS_TOKEN_EXPIRATION_MINUTES),
                    },
            key=SECRET_KEY,
            algorithm='HS256',
        )
        refresh_token = jwt.encode(
            payload={
                'user_id': user_id,
                'exp': get_expiry_time(
                    settings.REFRESH_TOKEN_EXPIRATION_MINUTES),
                    },
            key=SECRET_KEY,
            algorithm='HS256',
        )

        return access_token, refresh_token
