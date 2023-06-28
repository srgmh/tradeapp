from django.conf import settings
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, \
    SpectacularRedocView

import api_users.urls

urlpatterns = [
    path('', include(api_users.urls)),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            'schema/',
            SpectacularAPIView.as_view(),
            name='schema',
        ),
        path(
            'schema/swagger-ui/',
            SpectacularSwaggerView.as_view(url_name='schema'),
            name='swagger-ui',
        ),
        path(
            'schema/redoc/',
            SpectacularRedocView.as_view(url_name='schema'),
            name='redoc',
        ),
    ]
