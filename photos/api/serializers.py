"""
Serializers for all the models of photos
"""
from rest_framework import serializers

from photos.models import Album, Photo


class PhotoSerializer(serializers.ModelSerializer):
    """
    Serializer for photo
    """
    class Meta:
        model = Photo
        fields = ('id', 'title', 'image')


class AlbumWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating albums
    """
    photos = serializers.ListField(child=serializers.UUIDField(), write_only=True)

    class Meta:
        model = Album
        fields = ('id', 'name', 'photos')

    def validate_photos(self, attrs):
        """
        Check if all the photo ids are valid and belong to the current user
        """
        request = self.context.get('request')

        if Photo.objects.filter(id__in=attrs, owner=request.user).count() != len(attrs):
            raise serializers.ValidationError({'photos': 'Added invalid photos'})

        return attrs

    def to_representation(self, instance):
        """
        Display the primary keys only when an Album is being created/updated
        """
        self.fields['photos'] = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        representation = super(AlbumWriteSerializer, self).to_representation(instance)
        return representation


class AlbumDisplaySerializer(serializers.ModelSerializer):
    """
    Serializer for displaying albums
    """
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('id', 'name', 'photos')
