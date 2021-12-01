"""
Factories for the photos app
"""
import factory
from factory.django import DjangoModelFactory
from faker import Faker
from users.tests.factories import UserFactory

from photos.models import Album, Photo


class PhotoFactory(DjangoModelFactory):
    """
    Factory for BusinessLine model
    """

    class Meta:
        model = Photo
        django_get_or_create = ('title',)

    title = factory.Faker('word')
    owner = factory.SubFactory(UserFactory)
    image = Faker().mime_type(category='image')


class AlbumFactory(DjangoModelFactory):
    """
    Factory for BusinessLine model
    """

    class Meta:
        model = Album

    name = factory.Faker('word')
    photos = factory.RelatedFactoryList(PhotoFactory)
    owner = factory.SubFactory(UserFactory)
