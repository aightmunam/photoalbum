from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from photos.api.views import PhotoViewSet, AlbumViewSet


router = DefaultRouter()


router.register("photos", PhotoViewSet, basename='photo')
router.register("albums", AlbumViewSet, basename='album')


app_name = "api"

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^users/', include('users.api.urls')),
]
