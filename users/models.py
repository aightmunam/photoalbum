"""
Models for the users app
"""
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from model_utils.models import TimeStampedModel
from jsonfield.fields import JSONField
from collections import OrderedDict


class User(AbstractUser):
    """
    Custom user
    """

    def to_dict(self):
        """
        Dict representation to add to the logs
        """
        return {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    def get_absolute_url(self):
        """Get url for user's detail view.
        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def auth(self):
        return self.id


class UpdateHistory(TimeStampedModel):
    """
    Model so that we can maintain a history of changes.

    Fields:
        site (ForeignKey): foreign-key to User
        site_values (JSONField): json field to store history updates for a user
    """
    user = models.ForeignKey(
        User,
        related_name='update_histories',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    update_values = JSONField(
        null=False,
        blank=True,
        load_kwargs={'object_pairs_hook': OrderedDict}
    )
