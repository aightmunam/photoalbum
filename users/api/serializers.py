"""
Serializers for the users app
"""
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(ModelSerializer):
    """
    Serializer for user
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', ]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        """
        Check if both passwords are the same
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields do not match."})

        return attrs

    def create(self, validated_data):
        """
        Create a user object with the validated data
        """
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        user.set_password(validated_data.get('password'))
        user.save()

        return user
