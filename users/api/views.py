"""
All the api views for the users app
"""
from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User

from .permissions import IsOwnerOrAdmin
from .serializers import RegisterSerializer, UserSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    APIView to retrieve and update users. Only an admin
    or the user themselves can update their user object
    """
    queryset = User.objects.all()
    permission_classes = (IsOwnerOrAdmin,)
    serializer_class = UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    APIView to register a new user
    """
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
