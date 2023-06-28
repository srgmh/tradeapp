from django.contrib.auth import get_user_model
from django.conf import settings

from api_users.services.token_services import check_token

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
        '/api/users/profile/',
    )

    def __init__(self, get_response):
        self.get_response = get_response
        self.paths = self.include_paths

    def __call__(self, request):

        path = request.path
        if path not in self.paths:
            return self.get_response(request)

        response = check_token(request)
        if response:
            return response

        response = self.get_response(request)
        return response
