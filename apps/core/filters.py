import django_filters

from apps.albums.models import Album, FavoriteAlbum
from apps.artists.models import Artist, FavoriteArtist
from apps.audio.models import Track
from apps.playlists.models import FavoritePlaylist, Playlist


class TrackFilter(django_filters.FilterSet):
    class Meta:
        model = Track
        fields = {
            "genre__slug": ["exact"],
            "artist__slug": ["exact"],
            "album__slug": ["exact"],
        }


class MyTrackFilter(django_filters.FilterSet):
    class Meta:
        model = Track
        fields = {
            "genre__slug": ["exact"],
            "album__slug": ["exact"],
            "is_private": ["exact"],
        }


class ArtistFilter(django_filters.FilterSet):
    class Meta:
        model = Artist
        fields = {
            "is_verify": ["exact"],
        }


class AlbumFilter(django_filters.FilterSet):
    class Meta:
        model = Album
        fields = {
            "is_private": ["exact"],
            "artist__slug": ["exact"],
        }


class MyAlbumFilter(django_filters.FilterSet):
    class Meta:
        model = Album
        fields = {
            "is_private": ["exact"],
        }


class PlaylistFilter(django_filters.FilterSet):
    class Meta:
        model = Playlist
        fields = {
            "genre__slug": ["exact"],
            "user__id": ["exact"],
            "tracks__slug": ["exact"],
        }


class MyPlaylistFilter(django_filters.FilterSet):
    class Meta:
        model = Playlist
        fields = {
            "genre__slug": ["exact"],
            "user__id": ["exact"],
            "tracks__slug": ["exact"],
            "is_private": ["exact"],
        }


class FavoritePlaylistFilter(django_filters.FilterSet):
    class Meta:
        model = FavoritePlaylist
        fields = {
            "playlist__genre__slug": ["exact"],
            "user__id": ["exact"],
            "playlist__tracks__slug": ["exact"],
        }


class FavoriteAlbumFilter(django_filters.FilterSet):
    class Meta:
        model = FavoriteAlbum
        fields = {
            "album__artist__slug": ["exact"],
            "user__id": ["exact"],
            "album__tracks__slug": ["exact"],
        }


class FavoriteArtistFilter(django_filters.FilterSet):
    class Meta:
        model = FavoriteArtist
        fields = {
            "artist__slug": ["exact"],
            "user__id": ["exact"],
        }


