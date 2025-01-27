from typing import Dict, Union

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from crypto.models import Asset

User = get_user_model()


class AssetService:

    @staticmethod
    def get_asset(asset_id: int) -> Asset:
        try:
            return Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            raise ValidationError("Asset not found")

    @staticmethod
    def is_user_subscribed(asset: Asset, user: User):
        return asset.users.filter(id=user.id).exists()

    @staticmethod
    def subscribe(asset_id: int, user: User) -> Dict[str, Union[bool, str]]:
        if not asset_id:
            raise ValidationError("asset_id is required")

        asset = AssetService.get_asset(asset_id)

        if AssetService.is_user_subscribed(asset, user):
            return {
                'success': True,
                'message': 'You are already subscribed to this asset'
            }

        asset.users.add(user)

        return {
            'success': True,
            'message': 'Subscribed successfully.'
        }

    @staticmethod
    def unsubscribe(asset_id: int, user: User) -> Dict[str, Union[bool, str]]:
        if not asset_id:
            raise ValidationError("asset_id is required")

        asset = AssetService.get_asset(asset_id)

        if AssetService.is_user_subscribed(asset, user):
            asset.users.remove(user)
            return {
                'success': True,
                'message': 'Unsubscribed successfully.'
            }

        else:
            return {
                'success': True,
                'message': 'You are not subscribed to this asset.'
            }
