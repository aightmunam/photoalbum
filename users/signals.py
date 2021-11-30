"""
Receiver for signals
"""
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import photos.models

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
    log_update_history_task.delay(instance.auth, data)
