from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api_crypto.views import (AssetViewSet, OrderViewSet,
                              PostponedOrderViewSet, SuitcaseViewSet,
                              WalletViewSet)

router = SimpleRouter()
router.register(r'assets', AssetViewSet, basename='assets')
router.register(r'wallets', WalletViewSet, basename='wallets')
router.register(r'suitcases', SuitcaseViewSet, basename='suitcases')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'postponed_orders', PostponedOrderViewSet, basename='postponed_orders')


urlpatterns = [
    path('', include(router.urls)),
]
