from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from api_crypto.serializers import AssetSerializer
from api_users.authentication import SafeJWTAuthentication
from crypto.models import Asset


class AssetViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    authentication_classes = (SafeJWTAuthentication, )

    @action(methods=['post'], detail=False, url_path='subscribe')
    def subscribe(self, request: Request) -> Response:

        asset_id = request.data.get('asset_id', None)
        if not asset_id:
            raise ValidationError("asset_id are required.")

        try:
            asset = Asset.objects.get(id=asset_id)

            if asset.users.filter(id=request.user.id):
                return Response(
                    {'error': 'You are already subscribed to this asset'}
                )
        except Asset.DoesNotExist:
            return Response({'error': 'Asset not found'}, status=404)

        asset.users.add(request.user)

        return Response({'success': True})

    @action(methods=['post'], detail=False, url_path='unsubscribe')
    def unsubscribe(self, request):

        asset_id = request.data.get('asset_id', None)

        if not asset_id:
            raise ValidationError("asset_id is required.")

        try:
            asset = Asset.objects.get(id=asset_id)

            if asset.users.filter(id=request.user.id):
                asset.users.remove(request.user)
                return Response(
                    {'success': True, 'message': 'Unsubscribed successfully.'})
            else:
                return Response(
                    {'message': 'You are not subscribed to this asset.'})
        except Asset.DoesNotExist:
            return Response({'error': 'Asset not found'}, status=404)
