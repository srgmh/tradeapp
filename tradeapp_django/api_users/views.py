import jwt
from django.contrib.auth import authenticate, get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

from api_users.serializers import UserSerializer
from api_users.services.token_services import generate_jwt_token


User = get_user_model()
JWT_SECRET_KEY = settings.JWT_SECRET_KEY


class UserViewSet(viewsets.ViewSet):

    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'})
        return Response(serializer.errors, status=400)

    @action(methods=['post'], detail=False)
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user:
            access_token = generate_jwt_token(
                user.id, settings.ACCESS_TOKEN_EXPIRATION_MINUTES)
            refresh_token = generate_jwt_token(
                user.id, settings.REFRESH_TOKEN_EXPIRATION_MINUTES)

            return Response({
                'user_id': user.id,
                'access_token': access_token,
                'refresh_token': refresh_token})

        raise AuthenticationFailed('Invalid email or password')

    @action(methods=['post'], detail=False)
    def refresh_token(self, request):
        refresh_token = request.headers.get('Authorization')

        payload = jwt.decode(
            refresh_token, JWT_SECRET_KEY, algorithms=['HS256'])

        user_id = payload['user_id']

        access_token = generate_jwt_token(
            user_id, settings.ACCESS_TOKEN_EXPIRATION_MINUTES)
        refresh_token = generate_jwt_token(
            user_id, settings.REFRESH_TOKEN_EXPIRATION_MINUTES)

        return Response({
            'user_id': user_id,
            'access_token': access_token,
            'refresh_token': refresh_token
        })

    @action(methods=['get'], detail=False)
    def profile(self, request):
        token = request.headers.get('Authorization', None)
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        user = User.objects.filter(id=payload['user_id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)
