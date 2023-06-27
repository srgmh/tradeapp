from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path('', include('api_users.urls')),
    path('schema/',
         SpectacularAPIView.as_view(), name='schema'),
    path('docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
