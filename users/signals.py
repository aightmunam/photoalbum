"""
Receiver for signals
"""
import photos.models
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .tasks import log_update_history_task


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Post save signal to create a token whenever a user is created
    """
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=photos.models.Album)
@receiver(post_save, sender=photos.models.Photo)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_celery_task(sender, instance=None, created=False, **kwargs):
    """
    Post save signal handler to log all the updates to the db via
    a celery task
    """
    data = instance.to_dict()
    description = prepare_update_log_description(instance, status=created)
    log_update_history_task.delay(instance.auth, description, data)


@receiver(post_delete, sender=photos.models.Album)
@receiver(post_delete, sender=photos.models.Photo)
@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def send_celery_task(sender, instance=None, *args, **kwargs):
    """
    Post delete signal handler to log all the deletions to the db via
    a celery task
    """
    data = instance.to_dict()
    description = prepare_update_log_description(instance)
    log_update_history_task.delay(instance.auth, description, data)


def prepare_update_log_description(instance, status=None):
    """
    Prepare the description string for UpdateHistory object
    """
    model_name = instance._meta.model.__name__
    action = 'Created' if status else 'Updated'
    if status is None:
        action = 'Deleted'

    return f'{model_name} {action}: {instance.id}'
