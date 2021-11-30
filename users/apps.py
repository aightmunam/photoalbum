"""
App Config for the users app
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    App configuration for the users app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        try:
            import users.signals
        except ImportError:
            pass
