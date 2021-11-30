"""
Config for the photos app
"""
from django.apps import AppConfig


class PhotosConfig(AppConfig):
    """
    App config for photos app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'photos'
