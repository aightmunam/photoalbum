"""
All the api views for the photos app
"""
from django.http import Http404
from django.views.generic.detail import SingleObjectMixin
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, \
    CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet

from .permissions import IsAuthenticatedOwner
from .serializers import PhotoSerializer, AlbumDisplaySerializer, AlbumWriteSerializer
from rest_framework import viewsets, status
from django.contrib.auth import get_user_model

from ..models import Album

User = get_user_model()


class SetCurrentUserAsOwnerOnCreateUpdate:
    """
    Sets the current authenticated user as the owner when the
    object is updated or created
    """

    def perform_create(self, serializer):
        """
        Add the current user as the owner of the photo
        """
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """
        Add the current user as the owner of the photo
        """
        serializer.save(owner=self.request.user)


class PhotoViewSet(SetCurrentUserAsOwnerOnCreateUpdate, viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOwner,)

    def get_queryset(self):
        """
        Get all the photos of the logged in user
        """
        return self.request.user.photos.all()


class AlbumViewSet(SetCurrentUserAsOwnerOnCreateUpdate, ModelViewSet):
    """
    ViewSet for albums
    """
    model = Album
    permission_classes = (IsAuthenticatedOwner,)

    def get_serializer_class(self):
        """
        Return the serializer class based on the action
        """
        if self.action in ['list', 'retrieve']:
            return AlbumDisplaySerializer
        return AlbumWriteSerializer

    def get_queryset(self):
        """
        Get all the albums of the logged in user
        """
        return self.request.user.albums.all()

