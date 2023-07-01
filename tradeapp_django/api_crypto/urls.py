from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api_crypto.views import AssetViewSet

router = SimpleRouter()
router.register(r'assets', AssetViewSet, basename='assets')


urlpatterns = [
    path('', include(router.urls)),
]
