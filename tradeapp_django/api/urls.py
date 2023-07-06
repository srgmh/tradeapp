from django.conf import settings
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

import api_crypto.urls
import api_users.urls

urlpatterns = [
    path('', include(api_users.urls)),
    path('', include(api_crypto.urls))
]

if settings.DEBUG:
    urlpatterns += [
        path(
            'schema/',
            SpectacularAPIView.as_view(),
            name='schema',
        ),
        path(
            'docs/',
            SpectacularSwaggerView.as_view(url_name='schema'),
            name='swagger-ui',
        ),
        path(
            'schema/redoc/',
            SpectacularRedocView.as_view(url_name='schema'),
            name='redoc',
        ),
    ]
