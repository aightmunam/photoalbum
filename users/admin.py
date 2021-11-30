"""
Admin for the users app
"""
from django.contrib import admin

from .forms import UserChangeForm, UserCreationForm
from .models import UpdateHistory, User


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
