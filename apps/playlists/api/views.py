from django_filters import rest_framework as dj_filters
from rest_framework import generics, permissions, status, views
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.audio.models import Track
from apps.core import filters, pagination
from apps.core.permissions import IsOwnerUserPermission
from apps.playlists.api.serializers import (
    FavoritePlaylistSerializer,
    PlaylistSerializer,
    ShortPlaylistSerializer,
    UpdatePlaylistSerializer,
)
from apps.playlists.models import FavoritePlaylist, Playlist


class PlaylistListAPIView(generics.ListAPIView):
    """
    Playlist List API View.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ShortPlaylistSerializer
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.PlaylistFilter
    search_fields = ["user__display_name", "title", "tracks__title", "genre__name"]
    ordering_fields = ["release_date", "created_at"]

    def get_queryset(self):
        return Playlist.objects.select_related("user", "genre").prefetch_related("tracks").filter(is_private=False)


class PlaylistDetailAPIView(generics.RetrieveAPIView):
    """
    Playlist Detail API View. Public view.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PlaylistSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Playlist.objects.select_related("user", "genre").filter(is_private=False)


class MyPlaylistListCreateAPIView(generics.ListCreateAPIView):
    """
    My Playlist List Create API View.
    Private view, only for authenticated users and owner.
    """

    permission_classes = [IsOwnerUserPermission]
    serializer_class = PlaylistSerializer
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.MyPlaylistFilter
    search_fields = ["user__display_name", "title", "tracks__title", "genre__name"]
    ordering_fields = ["release_date", "created_at"]

    def get_queryset(self):
        return (
            Playlist.objects.select_related("user", "genre")
            .prefetch_related("tracks", "tracks__artist", "tracks__album", "tracks__genre")
            .filter(user=self.request.user)
        )

    def perform_create(self, serializer):
        playlist = serializer.save(user=self.request.user)
        FavoritePlaylist.objects.create(user=self.request.user, playlist=playlist)


class MyPlaylistDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    My Playlist Detail API View.
    Private view, only for authenticated users and owner.
    """

    permission_classes = [IsOwnerUserPermission]
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Playlist.objects.select_related("user", "genre")
            .prefetch_related("tracks", "tracks__artist", "tracks__album", "tracks__genre")
            .filter(user=self.request.user)
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PlaylistSerializer
        else:
            return UpdatePlaylistSerializer

    def perform_destroy(self, instance):
        FavoritePlaylist.objects.filter(user=self.request.user, playlist=instance).delete()
        instance.delete()


class PlaylistFavoriteListAPIView(generics.ListAPIView):
    """
    Favorite Playlist List API View.
    Private view, only for authenticated users and owner.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoritePlaylistSerializer
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.FavoritePlaylistFilter
    search_fields = ["user__display_name", "playlist__title", "playlist__tracks__title", "playlist__genre__name"]
    ordering_fields = ["playlist__release_date", "playlist__created_at"]

    def get_queryset(self):
        return FavoritePlaylist.objects.select_related("user", "playlist", "playlist__genre", "playlist__user").filter(
            user=self.request.user
        )


class PlaylistFavoriteCreateAPIView(views.APIView):
    """
    Favorite Playlist Create API View.
    Private view, only for authenticated users and owner.
    - `POST`: Add playlist to favorites.
    - `DELETE`: Remove playlist from favorites.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def post(self, request, *args, **kwargs):
        playlist = get_object_or_404(Playlist, slug=kwargs.get("slug"), is_private=False)
        favorite_playlist, created = FavoritePlaylist.objects.get_or_create(user=request.user, playlist=playlist)
        if not created:
            return Response({"msg": "Playlist already added to favorites"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Playlist added to favorites"}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        playlist = get_object_or_404(Playlist, slug=kwargs.get("slug"), is_private=False)
        favorite_playlist = get_object_or_404(FavoritePlaylist, user=request.user, playlist=playlist)
        favorite_playlist.delete()
        return Response({"msg": "Playlist removed from favorites"}, status=status.HTTP_204_NO_CONTENT)


class AddRemoveTrackPlaylistAPIView(views.APIView):
    """
    Add Remove Track Playlist API View.
    Private view, only for authenticated users and owner.
    - `POST`: Add track to playlist.
    - `DELETE`: Remove track from playlist.
    """

    permission_classes = [IsOwnerUserPermission]
    serializer_class = None

    def post(self, request, *args, **kwargs):
        playlist = get_object_or_404(Playlist, user=request.user, slug=kwargs.get("slug"))
        track = get_object_or_404(Track, slug=kwargs.get("track_slug"))
        if track in playlist.tracks.all():
            return Response({"msg": "Track already in playlist"}, status=status.HTTP_400_BAD_REQUEST)
        playlist.tracks.add(track)
        return Response({"msg": "Track added to playlist"}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        playlist = get_object_or_404(Playlist, user=request.user, slug=kwargs.get("slug"))
        track = get_object_or_404(Track, slug=kwargs.get("track_slug"))
        if track not in playlist.tracks.all():
            return Response({"msg": "Track not in playlist"}, status=status.HTTP_404_NOT_FOUND)
        playlist.tracks.remove(track)
        return Response({"msg": "Track removed from playlist"}, status=status.HTTP_204_NO_CONTENT)


