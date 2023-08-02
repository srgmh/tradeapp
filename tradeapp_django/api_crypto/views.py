from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from api_crypto.serializers import (AssetSerializer, OrderSerializer,
                                    PostponedOrderSerializer,
                                    SuitcaseSerializer, WalletSerializer)
from api_crypto.services.assest_service import AssetService
from api_crypto.services.order_service import OrderService
from api_crypto.services.postponedorder_service import PostponedOrderService
from api_users.authentication import SafeJWTAuthentication
from crypto.models import Order, PostponedOrder, Suitcase, Wallet, Asset


class AssetViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    serializer_class = AssetSerializer
    authentication_classes = (SafeJWTAuthentication, )
    queryset = Asset.objects.all()

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


class OrderViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    serializer_class = OrderSerializer
    authentication_classes = (SafeJWTAuthentication, )

    def get_queryset(self):
        """Get query set of orders created by current user."""
        return Order.objects.filter(user=self.request.user)

    @action(methods=['post'], detail=False, url_path='create_order')
    def create_order(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        operation_type = serializer.validated_data['operation_type']
        asset = serializer.validated_data['asset']
        quantity = serializer.validated_data['quantity']
        order = serializer.save(user=user)
        result = OrderService.create_order(
            user,
            order,
            operation_type,
            asset,
            quantity
        )

        return Response(result)


class PostponedOrderViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = PostponedOrderSerializer
    authentication_classes = (SafeJWTAuthentication,)

    def get_queryset(self):
        return PostponedOrder.objects.filter(user=self.request.user)

    @action(methods=['post'], detail=False, url_path='create_postponed_order')
    def create_postponed_order(self, request: Request):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        asset = serializer.validated_data['asset']
        if not asset.users.filter(id=user.id).exists():
            raise ValidationError("User is not a subscriber of the asset.")
        postponed_order = serializer.save(user=user)
        PostponedOrderService.create_task(postponed_order)

        return Response({'Postponed order created!': True})
