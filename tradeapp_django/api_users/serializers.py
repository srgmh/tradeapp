from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'is_blocked']
        read_only_fields = ('id', 'role', 'is_blocked')
        write_only_fields = ('password', )

    def create(self, validated_data):
        """Password hashing before saving to database."""

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
