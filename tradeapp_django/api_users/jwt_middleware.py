from django.conf import settings
from django.contrib.auth import get_user_model

from api_users.authentication import SafeJWTAuthentication

SECRET_KEY = settings.JWT_SECRET_KEY
User = get_user_model()


class JWTMiddleware:
    """
    Middleware to authenticate JWT token for specific paths.

    This middleware checks if the request path is included
    in the `include_paths` list.

    If included, it verifies the JWT token provided in the request headers
    and raises an `AuthenticationFailed` exception if the token is expired
    or invalid.
    """

    include_paths = (
        '/api/users/refresh_token/',
        '/api/assets/subscribe/'
    )

    def __init__(self, get_response):
        self.get_response = get_response
        self.paths = self.include_paths

    def __call__(self, request):

        if request.path in self.include_paths:
            request.user = SafeJWTAuthentication.authenticate(request)

        response = self.get_response(request)
        return response
