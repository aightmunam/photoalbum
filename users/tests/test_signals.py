"""
Test all the signals for the users app
"""
import mock
import pytest
from photos.tests.factories import AlbumFactory, PhotoFactory

from users.signals import prepare_update_log_description
from users.tests.factories import UserFactory


@mock.patch('users.signals.log_update_history_task')
@pytest.mark.django_db
def test_question_posted_signal_triggered(mock_task):
    """
    Test that the signal is emitted correctly when a user
    profile, or photo, or album is updated. Also, test
    that the data is sent correctly to the task
    """
    # Case where a user updates their profile
    user = UserFactory()
    assert mock_task.delay.called
    user_id, description, data_to_log = mock_task.delay.call_args.args
    assert user_id == user.id
    assert description == prepare_update_log_description(user, status=False)
    assert data_to_log == user.to_dict()

    # Case where a photo is updated
    photo = PhotoFactory()
    assert mock_task.delay.called
    user_id, description, data_to_log = mock_task.delay.call_args.args
    assert user_id == photo.owner.id
    assert description == prepare_update_log_description(photo, status=True)
    assert data_to_log == photo.to_dict()

    # Case where an album is updated
    album = AlbumFactory()
    assert mock_task.delay.called
    user_id, description, data_to_log = mock_task.delay.call_args.args
    assert user_id == album.owner.id
    assert description == prepare_update_log_description(album, status=False)
    assert data_to_log == album.to_dict()
