
from django_filters import rest_framework as dj_filters
from rest_framework import generics, permissions, status, views
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.albums.api.serializers import AlbumDetailSerializer, AlbumSerializer, FavoriteAlbumSerializer
from apps.albums.models import Album, FavoriteAlbum
from apps.core import filters, pagination
from apps.core.permissions import ArtistRequiredPermission

# Get List Album public (GET)
class GetAlbumListAPIView(generics.ListAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.AlbumFilter
    search_fields = ["artist__display_name", "title", "tracks__title"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return Album.objects.select_related("artist").filter(is_private=False)

# Get Detail Album public (GET)
class GetAlbumDetailAPIView(generics.RetrieveAPIView):
    serializer_class = AlbumDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Album.objects.select_related("artist").filter(is_private=False)

# Get My List Album (GET)
class GetMyAlbumListAPIView(generics.ListAPIView):
    serializer_class = AlbumDetailSerializer
    permission_classes = [ArtistRequiredPermission]
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.MyAlbumFilter
    search_fields = ["artist__display_name", "title", "tracks__title"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return Album.objects.select_related("artist").filter(artist=self.request.user.artist)

# Create My Album (POST)
class CreateMyAlbumAPIView(generics.CreateAPIView):
    serializer_class = AlbumDetailSerializer
    permission_classes = [ArtistRequiredPermission]

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user.artist)

# Get Detail My Album
class GetMyAlbumDetailAPIView(generics.RetrieveAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [ArtistRequiredPermission]
    lookup_field = "slug"

    def get_queryset(self):
        return Album.objects.select_related("artist").filter(artist=self.request.user.artist)

# Update Detail My Album
class UpdateMyAlbumDetailAPIView(generics.UpdateAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [ArtistRequiredPermission]
    lookup_field = "slug"

    def get_queryset(self):
        return Album.objects.filter(artist=self.request.user.artist)

# Delete Detail My Album
class DeleteMyAlbumDetailAPIView(generics.DestroyAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [ArtistRequiredPermission]
    lookup_field = "slug"

    def get_queryset(self):
        return Album.objects.filter(artist=self.request.user.artist)

# Get List Album Favorite (GET)
class GetAlbumFavoriteListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteAlbumSerializer
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.FavoriteAlbumFilter
    search_fields = ["user__display_name", "album__title", "album__tracks__title", "album__artist__display_name"]
    ordering_fields = ["album__release_date", "album__created_at"]

    def get_queryset(self):
        return FavoriteAlbum.objects.select_related("user", "album", "album__artist", "album__artist__user").filter(
            user=self.request.user
        )

# Create Album Favorite (POST)
class AlbumFavoriteCreateAPIView(views.CreateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def post(self, request, *args, **kwargs):
        album = get_object_or_404(Album, slug=kwargs.get("slug"), is_private=False)

        favorite_album, created = FavoriteAlbum.objects.get_or_create(user=request.user, album=album)

        if not created:
            return Response({"msg": "Album already added to favorites"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Album added to favorites"}, status=status.HTTP_201_CREATED)

# Delete Album Favorite (DELETE)
class AlbumFavoriteDeleteAPIView(views.DestroyAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def delete(self, request, *args, **kwargs):
        album = get_object_or_404(Album, slug=kwargs.get("slug"), is_private=False)

        favorite_album = get_object_or_404(FavoriteAlbum, user=request.user, album=album)

        favorite_album.delete()
        
        return Response({"msg": "Album removed from favorites"}, status=status.HTTP_204_NO_CONTENT)


