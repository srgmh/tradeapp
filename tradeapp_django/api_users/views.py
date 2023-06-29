from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api_users.serializers import UserSerializer
from api_users.services.token_services import (SafeJWTAuthentication,
                                               generate_token)

User = get_user_model()
JWT_SECRET_KEY = settings.JWT_SECRET_KEY


class UserViewSet(viewsets.ViewSet):

    serializer_class = UserSerializer

    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'User created!': serializer.data})

    @action(methods=['post'], detail=False, url_path='login')
    def login(self, request: Request) -> Response:
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        access_token, refresh_token = (
            generate_token(
                user.id, settings.ACCESS_TOKEN_EXPIRATION_MINUTES),
            generate_token(
                user.id, settings.REFRESH_TOKEN_EXPIRATION_MINUTES))

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_id': UserSerializer(user).data})

    @action(methods=['get'], detail=False, url_path='refresh_token')
    def refresh_token(self, request: Request) -> Response:

        access_token, refresh_token = (
            generate_token(
                request.user.id, settings.ACCESS_TOKEN_EXPIRATION_MINUTES),
            generate_token(
                request.user.id, settings.REFRESH_TOKEN_EXPIRATION_MINUTES))

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_id': UserSerializer(request.user).data
        })
