from django.urls import include, path
import api_users.urls

urlpatterns = [
    path('', include(api_users.urls)),
]
