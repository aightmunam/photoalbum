from django.contrib import admin

from .models import Photo, Album


@admin.register(Photo, Album)
class PhotoAdmin(admin.ModelAdmin):
    pass
