from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api_crypto.serializers import (AssetSerializer, OrderSerializer,
                                    SuitcaseSerializer, WalletSerializer)
from api_crypto.services.assest_service import AssetService
from api_crypto.services.order_service import OrderService
from api_users.authentication import SafeJWTAuthentication
from crypto.models import Order, Suitcase, Wallet


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
    def unsubscribe(self, request: Request) -> Response:

        asset_id = request.data.get('asset_id', None)
        result = AssetService.unsubscribe(asset_id, request.user)

        return Response(result)


class WalletViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = WalletSerializer
    authentication_classes = (SafeJWTAuthentication, )

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(suitcase__user=user)


class SuitcaseViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    serializer_class = SuitcaseSerializer
    authentication_classes = (SafeJWTAuthentication,)

    def get_queryset(self):
        user = self.request.user
        return Suitcase.objects.filter(user=user)


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    serializer_class = OrderSerializer
    authentication_classes = (SafeJWTAuthentication, )

    def get_queryset(self):
        """Get query set of orders created by current user."""

        return Order.objects.filter(user=self.request.user)

    def perform_create(self, request: Request):

        operation_type = request.data.get('operation_type', None)
        asset = request.data.get('asset', None)
        quantity = request.data.get('quantity', None)
        user = self.request.user
        serializer = self.get_serializer(data=request.data)

        OrderService.create_order(serializer, user, operation_type, asset, quantity)

