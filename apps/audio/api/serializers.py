from rest_framework import serializers

from apps.albums.models import Album
from apps.artists.api.serializers import ShortArtistSerializer
from apps.audio.models import Track
from apps.genre.api.serializers import GenreSerializer
from apps.genre.models import Genre


class ShortAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = [
            "id",
            "slug",
            "title",
            "image",
            "color",
            "is_private",
        ]

class TrackSerializer(serializers.ModelSerializer):
    artist = ShortArtistSerializer(read_only=True, many=False)
    genre = GenreSerializer(read_only=True, many=False)
    album = ShortAlbumSerializer(read_only=True, many=False)

    class Meta:
        model = Track
        fields = [
            "id",
            "slug",
            "artist",
            "title",
            "duration",
            "image",
            "color",
            "genre",
            "album",
            "file",
            "plays_count",
            "downloads_count",
            "likes_count",
            "user_of_likes",
            "is_private",
            "release_date",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "plays_count": {"read_only": True},
            "downloads_count": {"read_only": True},
            "likes_count": {"read_only": True},
            "user_of_likes": {"read_only": True},
            "duration": {"read_only": True},
            "color": {"read_only": True},
        }

class ShortTrackSerializer(TrackSerializer):
    class Meta:
        model = Track
        fields = [
            "id",
            "slug",
            "artist",
            "title",
            "file",
            "duration",
            "image",
            "color",
            "plays_count",
            "genre",
            "album",
        ]

class TrackCreateSerializer(TrackSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all(), required=False)
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())