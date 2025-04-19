from django_filters import rest_framework as dj_filters
from rest_framework import generics, permissions, status, views
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response


from apps.artists.models import Artist, ArtistVerificationRequest, FavoriteArtist, License
from apps.core import filters, pagination
from apps.core.permissions import ArtistRequiredPermission, IsPremiumUserPermission

from .serializers import ArtistSerializer, FavoriteArtistSerializer, LicenseSerializer, UpdateArtistImageSerializer

# Get List Artist (GET)
class GetArtistListAPIView(generics.ListAPIView):
    # Get artistList with filter
    
    # query get all artist with Join "user" infor related
    queryset = Artist.objects.select_related("user").all()
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.StandardResultsSetPagination
    # Apply serializer to convert data response => Json structure
    serializer_class = ArtistSerializer
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    # dj_filters.DjangoFilterBackend: filterset_class
    # SearchFilter: search_fields
    # OrderingFilter: ordering_fields
    filterset_class = filters.ArtistFilter
    search_fields = ["display_name", "first_name", "last_name"]
    ordering_fields = ["created_at"]

# Create Artist (POST)
class CreateArtistAPIView(generics.CreateAPIView):
    # Create a artist
    queryset = Artist.objects.select_related("user").all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Detail Artists (GET)
class GetDetailArtistAPIView(generics.RetrieveAPIView):
    # lazy query
    queryset = Artist.objects.select_related("user").all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

# Get Detail My Artist (GET)
class GetArtistDetailMeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ArtistSerializer
    permission_classes = [ArtistRequiredPermission]

    def get_object(self):
        return self.request.user.artist

# Get List Artist Favorite (GET)
class GetArtistFavoriteListAPIView(generics.ListAPIView):
    """
    Favorite Artist List API View.
    Private view, only for authenticated users and owner.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteArtistSerializer
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.FavoriteArtistFilter
    search_fields = ["user__display_name", "artist__display_name"]
    ordering_fields = ["artist__created_at"]

    def get_queryset(self):
        return FavoriteArtist.objects.select_related("user", "artist", "artist__user").filter(user=self.request.user)

# Create Artist To Favorite List (POST)
class ArtistFavoriteCreateAPIView(views.APIView):
    """
    Favorite Artist Create API View.
    Private view, only for authenticated users and owner.
    - `POST`: Add artist to favorites.
    1. If artist already in favorites, return `HTTP_400_BAD_REQUEST.
    2. If artist not in favorites, create new favorite and return `HTTP_201_CREATED`.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def post(self, request, *args, **kwargs):
     
        artist = get_object_or_404(Artist, slug=kwargs.get("slug"))

        favorite_playlist, created = FavoriteArtist.objects.get_or_create(user=request.user, artist=artist)

        if not created:
            return Response({"msg": "Artist already added to favorites"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Artist added to favorites"}, status=status.HTTP_201_CREATED)

# Delete Artist From Favorite List (DELETE)
class ArtistFavoriteDeleteAPIView(views.APIView):
    """
    Favorite Artist Create API View.
    Private view, only for authenticated users and owner.
    - `DELETE`: Remove artist from favorites.
    1. If artist not in favorites, return `HTTP_404_NOT_FOUND`.
    2. If artist in favorites, delete favorite and return `HTTP_204_NO_CONTENT`.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def delete(self, request, *args, **kwargs):

        artist = get_object_or_404(Artist, slug=kwargs.get("slug"))

        favorite_playlist = get_object_or_404(FavoriteArtist, user=request.user, artist=artist)

        favorite_playlist.delete()
        
        return Response({"msg": "Artist removed from favorites"}, status=status.HTTP_204_NO_CONTENT)

