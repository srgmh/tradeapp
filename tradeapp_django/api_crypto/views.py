
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api_crypto.serializers import AssetSerializer
from crypto.models import Asset


class AssetViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    @action(methods=['post'], detail=False, url_path='subscribe')
    def subscribe(self, request):

        asset_id = request.data.get('asset_id', None)
        if not asset_id:
            raise ValidationError("asset_id are required.")

        try:
            asset = Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            return Response({'error': 'Asset not found'}, status=404)

        asset.users.add(request.user)

        return Response({'success': True})

    def unsubscribe(self):
        pass
