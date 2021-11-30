"""
Test that the serializer works correctly
"""
import pytest
from django.urls import reverse
from rest_framework import status

from users.tests.factories import UserFactory

from .factories import AlbumFactory

JSON_CONTENT_TYPE = 'application/json'


@pytest.fixture
def user_instance(request):
    """
    Create user, this fixture can be passed as a parameter to other pytests or fixtures
    """
    return UserFactory(password='password')


@pytest.fixture
def logged_in_client(request, client, user_instance):
    """
    User login fixture. User will be authenticated for all tests where we pass this fixture.
    """
    client.login(username=user_instance.username, password='password')
    client.user = user_instance
    return client


@pytest.mark.django_db
def test_album_rename(logged_in_client):
    """
    Test that album can be created successfully via post
    """
    album = AlbumFactory(owner=logged_in_client.user)

    changed_name = 'Test Change'
    response = logged_in_client.patch(
        reverse('api:album-detail', kwargs={'pk': album.pk}),
        data={'name': changed_name},
        content_type=JSON_CONTENT_TYPE
    )

    album.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert album.name == changed_name

