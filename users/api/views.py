from rest_framework.permissions import AllowAny, IsAdminUser

from users.models import User
from .serializers import UserSerializer
from .serializers import RegisterSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework import generics


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

