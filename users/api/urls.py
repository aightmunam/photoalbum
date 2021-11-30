"""
Local urls for the users apis
"""
from django.urls import path

from .views import RegisterView, UserRetrieveUpdateDestroyView

app_name = "users"
urlpatterns = [
    path('register/new', RegisterView.as_view(), name='register'),
    path('<pk>', UserRetrieveUpdateDestroyView.as_view(), name='detail'),
]
