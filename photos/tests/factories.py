import factory
from faker import Faker
from faker.providers import file
from factory.django import DjangoModelFactory
from django.core.files.base import ContentFile

from photos.models import Photo, Album
from users.tests.factories import UserFactory


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

