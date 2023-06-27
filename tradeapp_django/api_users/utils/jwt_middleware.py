import jwt
from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

SECRET_KEY = settings.JWT_SECRET_KEY


class JWTMiddleware(MiddlewareMixin):

    exclude_paths = ['/api/register/', '/api/login/',
                     '/api/docs/', '/api/schema/']

    def process_request(self, request):

        path = request.path
        if path in self.exclude_paths:
            return None

        jwt_token = request.headers.get('authorization', None)

        if jwt_token:

            try:
                payload = jwt.decode(
                    jwt_token, SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return HttpResponse(
                    "Authentication token has expired",
                    status=401)
            except (jwt.DecodeError, jwt.InvalidTokenError):
                return HttpResponse(
                    'Authorization has failed, Please send valid token.',
                    status=401)

        else:
            return HttpResponse(
                'Authorization not found, Please send valid token in headers',
                status=401)
