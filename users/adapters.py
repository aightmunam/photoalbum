"""
Adapter for django-allauth to use
"""

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter for the Django AllAuth package
    """

    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
