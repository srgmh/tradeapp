import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

SECRET_KEY = settings.JWT_SECRET_KEY
User = get_user_model()


def generate_jwt_token(user_id, minutes_valid):
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


def check_token(request):
    """
    Checks if token is valid.
    """

    jwt_token = request.headers.get('Authorization', None)

    if jwt_token:
        try:
            payload = jwt.decode(
                jwt_token, SECRET_KEY, algorithms=['HS256'])

            user_id = payload.get('user_id')

            try:
                user = User.objects.get(id=user_id)
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
