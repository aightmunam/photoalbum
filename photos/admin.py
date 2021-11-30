"""
Admin for the photos app
"""
from django.contrib import admin

from .models import Album, Photo


@admin.register(Photo, Album)
class PhotoAdmin(admin.ModelAdmin):
    """
    Admin for Photo and Album models
    """
    pass
