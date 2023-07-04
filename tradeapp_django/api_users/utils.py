from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

SECRET_KEY = settings.JWT_SECRET_KEY
User = get_user_model()


def generate_token(user_id: int, minutes: int) -> str:
    """
    Generate JWT tokens by user_id and token expiration time.
    """

    expiry_time = datetime.utcnow() + timedelta(minutes=minutes)
    token = jwt.encode(
        payload={
            'user_id': user_id,
            'exp': expiry_time
        },
        key=SECRET_KEY,
        algorithm='HS256'
    )

    return token
