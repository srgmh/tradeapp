from typing import Optional
from urllib.request import Request

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

SECRET_KEY = settings.JWT_SECRET_KEY
User = get_user_model()


class SafeJWTAuthentication:

    @staticmethod
    def authenticate(request: Request) -> Optional[User]:
        """
        Checks if token is valid, return user object.
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
