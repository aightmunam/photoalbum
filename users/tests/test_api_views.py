"""
Test the users api
"""

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_403_FORBIDDEN

from users.api.constants import DUPLICATE_EMAIL, DUPLICATE_USERNAME, DUMMY_NAME, JSON_CONTENT_TYPE
from users.tests.factories import UserFactory


@pytest.mark.django_db
@pytest.mark.parametrize('username, password, confirm_password, email, expected_response', [
    ('test_user', 'dummy_password', 'dummy_password', 'test@example.com', HTTP_201_CREATED),
    ('test_user', 'dummy_password+1', 'dummy_password+2', 'test@example.com', HTTP_400_BAD_REQUEST),
    (DUPLICATE_USERNAME, 'dummy_password', 'dummy_password', 'test@example.com', HTTP_400_BAD_REQUEST),
    ('test_user', 'dummy_password', 'dummy_password', '', HTTP_400_BAD_REQUEST),
    ('test_user', 'dummy_password', 'dummy_password', DUPLICATE_EMAIL, HTTP_400_BAD_REQUEST),
], ids=[
    'all-fields-valid',
    'passwords-do-not-match',
    'duplicate-username-provided',
    'no-email-provided',
    'duplicate-email-provided'
])
def test_user_register_api(client, username, password, confirm_password, email, expected_response):
    """
    Test that the user can be created
    """
    UserFactory(username=DUPLICATE_USERNAME, email=DUPLICATE_EMAIL)

    response = client.post(
        reverse('api:users:register'),
        data={
            'username': username,
            'password': password,
            'password2': confirm_password,
            'email': email,
        },
    )

    assert response.status_code == expected_response


@pytest.mark.django_db
@pytest.mark.parametrize('method', ['put', 'patch', 'get'])
@pytest.mark.parametrize('is_owner, is_admin, expected_response', [
    (True, False, HTTP_200_OK),
    (False, True, HTTP_200_OK),
    (True, True, HTTP_200_OK),
    (False, False, HTTP_403_FORBIDDEN),
],  ids=[
    'self-account',
    'admin-user',
    'both-admin-and-self',
    'neither-admin-nor-self'
])
def test_user_update_api(client, is_owner, is_admin, expected_response, method):
    """
    Test that only the user themselves or an admin user should be able to update/retrieve a user
    """
    user_to_update = UserFactory()
    other_user = UserFactory(is_staff=is_admin)

    login_user = other_user
    if is_owner:
        login_user = user_to_update

    client.force_login(login_user)

    action = getattr(client, method)
    response = action(
        reverse('api:users:detail', kwargs={'pk': user_to_update.pk}),
        data={
            'first_name': DUMMY_NAME,
            'last_name': DUMMY_NAME,
            'username': user_to_update.username,
            'email': user_to_update.email
        },
        content_type=JSON_CONTENT_TYPE
    )

    user_to_update.refresh_from_db()

    assert response.status_code == expected_response
    if method in ['put', 'patch'] and expected_response == HTTP_200_OK:
        assert user_to_update.first_name == DUMMY_NAME
        assert user_to_update.last_name == DUMMY_NAME

