from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api_crypto.views import AssetViewSet, SuitcaseViewSet, WalletViewSet

router = SimpleRouter()
router.register(r'assets', AssetViewSet, basename='assets')
router.register(r'wallets', WalletViewSet, basename='wallets')
router.register(r'suitcases', SuitcaseViewSet, basename='suitcases')


urlpatterns = [
    path('', include(router.urls)),
]
