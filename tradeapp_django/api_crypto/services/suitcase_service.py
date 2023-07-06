from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from crypto.models import Suitcase


class SuitcaseService:

    @staticmethod
    def get_suitcase(user: get_user_model()) -> Suitcase:
        try:
            return Suitcase.objects.get(user=user)
        except Suitcase.DoesNotExist:
            raise ValidationError('Suitcase not found')
