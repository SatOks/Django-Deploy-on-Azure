from django.urls import path, include

urlpatterns = [
    path('api/', include('boards.urls.api')),
    path('', include('boards.urls.web')),
]

from .urls import urlpatterns  # noqa

__all__ = ['urlpatterns']