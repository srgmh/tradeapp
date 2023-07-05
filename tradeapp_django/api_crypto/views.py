from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api_crypto.serializers import (AssetSerializer, SuitcaseSerializer,
                                    WalletSerializer)
from api_crypto.services.AssestService import AssetService
from api_users.authentication import SafeJWTAuthentication
from crypto.models import Suitcase, Wallet


class AssetViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    serializer_class = AssetSerializer
    authentication_classes = (SafeJWTAuthentication, )

    @action(methods=['post'], detail=False, url_path='subscribe')
    def subscribe(self, request: Request) -> Response:

        asset_id = request.data.get('asset_id', None)
        result = AssetService.subscribe(asset_id, request.user)

        return Response(result)

    @action(methods=['post'], detail=False, url_path='unsubscribe')
    def unsubscribe(self, request):

        asset_id = request.data.get('asset_id', None)
        result = AssetService.unsubscribe(asset_id, request.user)

        return Response(result)


class WalletViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = WalletSerializer
    authentication_classes = (SafeJWTAuthentication, )

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(suitcase__user=user)


class SuitcaseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = SuitcaseSerializer
    authentication_classes = (SafeJWTAuthentication,)

    def get_queryset(self):
        user = self.request.user
        return Suitcase.objects.filter(user=user)
