from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.audio.api.serializers import ShortTrackSerializer
from apps.genre.api.serializers import GenreSerializer
from apps.genre.models import Genre
from apps.playlists.models import FavoritePlaylist, Playlist
from apps.users.api.serializers import ShortCustomUserSerializer


class PlaylistSerializer(serializers.ModelSerializer):
    user = ShortCustomUserSerializer(read_only=True, many=False)
    genre = GenreSerializer(read_only=True, many=False)
    tracks = ShortTrackSerializer(many=True, read_only=True)
    duration = serializers.DurationField(source="total_duration", read_only=True)
    favorite_count = serializers.IntegerField(source="get_favorite_count", read_only=True)

    class Meta:
        model = Playlist
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "image",
            "user",
            "tracks",
            "genre",
            "release_date",
            "is_private",
            "duration",
            "favorite_count",
            "created_at",
            "updated_at",
        ]


class UpdatePlaylistSerializer(PlaylistSerializer):
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), required=False)

    class Meta:
        model = Playlist
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "image",
            "genre",
            "release_date",
            "is_private",
        ]


class ShortPlaylistSerializer(PlaylistSerializer):
    track_slug = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Playlist
        fields = [
            "id",
            "slug",
            "title",
            "image",
            "user",
            "genre",
            "track_slug",
            "is_private",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_track_slug(self, obj):
        track = obj.tracks.first()
        if track:
            return track.slug


class FavoritePlaylistSerializer(serializers.ModelSerializer):
    playlist = ShortPlaylistSerializer(read_only=True, many=False)

    class Meta:
        model = FavoritePlaylist
        fields = ["id", "playlist", "created_at", "updated_at"]