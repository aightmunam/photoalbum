"""
Admin for the users app
"""
from django.contrib import admin

from .models import User, UpdateHistory
from .forms import UserChangeForm, UserCreationForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin for User model
    """
    list_display = ['username', 'email', 'last_login', 'date_joined', ]
    form = UserChangeForm
    add_form = UserCreationForm


@admin.register(UpdateHistory)
class UpdateHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'modified']
