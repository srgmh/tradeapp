from datetime import datetime, timedelta
from typing import Optional

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

SECRET_KEY = settings.JWT_SECRET_KEY
User = get_user_model()


class SafeJWTAuthentication:

    @staticmethod
    def authenticate(request) -> Optional[User]:
        """
        Checks if token is valid: return user object.
        """

        jwt_token = request.headers.get('Authorization', None)

        if jwt_token:
            try:
                payload = jwt.decode(
                    jwt_token, SECRET_KEY, algorithms=['HS256'])

                try:
                    user = User.objects.filter(id=payload['user_id']).first()
                    return user

                except User.DoesNotExist:
                    raise AuthenticationFailed(
                        'User does not exist')

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed(
                    'Authentication token has expired')

            except (jwt.DecodeError, jwt.InvalidTokenError):
                raise AuthenticationFailed(
                    'Authorization has failed. '
                    'Please send a valid token.')

        else:
            raise AuthenticationFailed(
                'Authorization not found. '
                'Please send a valid token in headers.')

    @staticmethod
    def generate_token(user_id: int, minutes_valid: int) -> str:
        """
        Generate JWT token by user_id and token expiration time.
        """

        expiry_time = datetime.utcnow() + timedelta(minutes=minutes_valid)
        payload = {
            'user_id': user_id,
            'exp': expiry_time,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return token
