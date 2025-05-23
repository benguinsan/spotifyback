import os.path

from django.http import FileResponse, Http404
from django_filters import rest_framework as dj_filters
from rest_framework import generics, permissions, status, views
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.audio.api.serializers import ShortTrackSerializer, TrackCreateSerializer, TrackSerializer
from apps.audio.models import Track
from apps.core import filters, pagination
from apps.core.permissions import ArtistRequiredPermission

# Get List Track (GET)
class TrackListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ShortTrackSerializer
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.TrackFilter
    search_fields = ["title", "artist__display_name", "genre__name", "album__title"]
    ordering_fields = ["release_date", "created_at", "plays_count", "downloads_count", "likes_count"]

    def get_queryset(self):
        return Track.objects.select_related("artist", "genre", "album").filter(is_private=False)

# Get List Track Liked (GET)
class TrackLikedListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShortTrackSerializer
    pagination_class = pagination.LargeResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.TrackFilter
    search_fields = ["title", "artist__display_name", "genre__name", "album__title"]
    ordering_fields = ["release_date", "created_at", "plays_count", "downloads_count", "likes_count"]

    def get_queryset(self):
        return Track.objects.select_related("artist", "genre", "album").filter(
            user_of_likes=self.request.user
        )

# Get, Post List Track Liked (GET, POST)
class TrackDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TrackSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Track.objects.select_related("artist", "genre", "album").filter(is_private=False)

# Get, Post List Recently Played Track (GET, POST)
class TrackRecentlyPlayedAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ShortTrackSerializer
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.TrackFilter
    search_fields = ["title", "artist__display_name", "genre__name", "album__title"]
    ordering_fields = ["release_date", "created_at", "plays_count", "downloads_count", "likes_count"]

    def get_queryset(self):
        viewer_ip = self.request.META.get("REMOTE_ADDR", None)

        if self.request.user.is_authenticated:
            return (
                Track.objects.select_related("artist", "genre", "album")
                .filter(is_private=False, plays__user=self.request.user)
                .order_by("-plays__played_at")[:10]
            )

        if viewer_ip:
            return (
                Track.objects.select_related("artist", "genre", "album")
                .filter(is_private=False, plays__viewer_ip=viewer_ip)
                .order_by("-plays__played_at")[:10]
            )

        return Track.objects.none()

# Get List Track Recently Played By User (GET)
class TrackRecentlyPlayedByUserAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ShortTrackSerializer
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.TrackFilter
    search_fields = ["title", "artist__display_name", "genre__name", "album__title"]
    ordering_fields = ["release_date", "created_at", "plays_count", "downloads_count", "likes_count"]
    lookup_field = "id"

    def get_queryset(self):
        last_played = (
            Track.objects.select_related("artist", "genre", "album")
            .filter(is_private=False, plays__user=self.kwargs.get("id", None))
            .order_by("-plays__played_at")[:10]
        )

        return last_played

# Get, Post List My Track (GET, POST)
class TrackMyListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [ArtistRequiredPermission]
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.MyTrackFilter
    search_fields = ["title", "genre__name", "album__title"]
    ordering_fields = ["release_date", "created_at", "plays_count", "downloads_count", "likes_count"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TrackCreateSerializer
        return TrackSerializer

    def get_queryset(self):
        return (
            Track.objects.select_related("artist", "genre", "album")
            .prefetch_related("user_of_likes")
            .filter(artist=self.request.user.artist)
        )

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user.artist)

# Get, Put, Delete My Track (GET, PUT, DELETE)
class TrackMyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ArtistRequiredPermission]
    serializer_class = TrackCreateSerializer
    lookup_field = "slug"

    def get_object(self):
        return (
            Track.objects.select_related("artist")
            .prefetch_related("user_of_likes")
            .get(slug=self.kwargs.get("slug"), artist=self.request.user.artist)
        )

# Streaming track (GET)
class StreamingTrackAPIView(views.APIView):
    serializer_class = None
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get"]

    def get_object(self):
        return get_object_or_404(Track, slug=self.kwargs.get("slug"), is_private=False)

    @staticmethod
    def set_play(track):
        track.plays_count += 1
        track.save()

    def get(self, request, *args, **kwargs):
        track = self.get_object()
        
        if os.path.exists(track.file.path):
            self.set_play(track)
            
            return FileResponse(open(track.file.path, "rb"), filename=track.file.name)
        else:
            raise Http404()


# Streaming track (GET)
class StreamingMyTrackAPIView(StreamingTrackAPIView):
    """
    Listen my track.
    """

    permission_classes = [ArtistRequiredPermission]
    http_method_names = ["get"]

    def get_object(self):
        return get_object_or_404(Track, slug=self.kwargs.get("slug"), artist=self.request.user.artist)


# Download track (GET)
class DownloadTrackAPIView(views.APIView):
    """Download track."""

    serializer_class = None
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get"]

    @staticmethod
    def set_download(track):
        track.downloads_count += 1
        track.save()

    def get(self, request, *args, **kwargs):
        track = get_object_or_404(Track, slug=self.kwargs.get("slug"), is_private=False)
        if os.path.exists(track.file.path):
            self.set_download(track)
            response = FileResponse(open(track.file.path, "rb"), as_attachment=True)
            response["Content-Disposition"] = f'attachment; filename="{track.file.name}"'
            response["X-Filename"] = track.file.name
            return response
        else:
            return Http404


# Like/Unlike track (POST, DELETE)
class TrackLikeUnlikeAPIView(views.APIView):
    """
    Like/Unlike track. Only for authenticated user.
    - `POST`: Like track.
    1. If user has not liked the track, add the like and increase the likes count and return status `HTTP_200_OK`.
    2. If user has already liked the track, return a message and status `HTTP_400_BAD_REQUEST`.
    - `DELETE`: Unlike track.
    1. If user has not liked the track, return a message and status `HTTP_400_BAD_REQUEST`.
    2. If user has liked the track, remove the like and decrease the likes count and return status `HTTP_200_OK`.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None
    http_method_names = ["post", "delete"]

    def get_object(self):
        return get_object_or_404(Track, slug=self.kwargs.get("slug"), is_private=False)

    def post(self, request, *args, **kwargs):
        track = self.get_object()
        if request.user not in track.user_of_likes.all():
            track.likes_count += 1
            track.user_of_likes.add(request.user)
            track.save()
            return Response({"likes_count": track.likes_count}, status.HTTP_200_OK)
        # If user has already liked the track, return a message
        return Response({"msg": "You have already liked this track."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        track = self.get_object()
        if request.user in track.user_of_likes.all():
            track.user_of_likes.remove(request.user)
            track.likes_count -= 1
            track.save()
            return Response({"likes_count": track.likes_count}, status.HTTP_200_OK)
        return Response({"msg": "You have not liked this track."}, status=status.HTTP_400_BAD_REQUEST)



