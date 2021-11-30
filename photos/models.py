"""
Models for the photos app
"""
import os
import uuid

from django.db import models
from model_utils.models import TimeStampedModel


def get_upload_location(instance, filename):
    _, extension = os.path.splitext(filename)
    return f'{instance.owner.username}/{instance.title}{extension}'


class Photo(TimeStampedModel):
    """
    Model to represent a photo
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to=get_upload_location, null=False, blank=False)
    owner = models.ForeignKey('users.User', related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}  ({self.title} - {self.owner})'

    def to_dict(self):
        """
        Dict representation to add to the logs
        """
        return {
            'id': self.id,
            'title': self.title,
            'image': self.image.path,
            'owner': self.owner.username
        }

    @property
    def auth(self):
        return self.owner.id


class Album(TimeStampedModel):
    """
    Model for the photo albums
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=150, blank=True)
    owner = models.ForeignKey('users.User', related_name='albums', on_delete=models.CASCADE)

    # allowing empty albums
    photos = models.ManyToManyField(Photo, related_name='albums')

    def __str__(self):
        return f'{self.id} ({self.name} - {self.owner})'

    def to_dict(self):
        """
        Dict representation to add to the logs
        """
        return {
            'id': self.id,
            'name': self.name,
            'owner': self.owner.username,
            'photos': list(self.photos.values_list('id', flat=True))
        }

    @property
    def auth(self):
        return self.owner.id
