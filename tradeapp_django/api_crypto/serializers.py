from rest_framework import serializers

from api_users.serializers import UserSerializer
from crypto.models import Asset


class AssetSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Asset
        fields = ('id', 'abbreviation', 'price', 'type', 'users', )
