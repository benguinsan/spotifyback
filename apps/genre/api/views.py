from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.core import pagination
from apps.other.api.serializers import GenreSerializer
from apps.other.models import Genre

# Get GenreList (GET)
class GetGenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.MaxResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["created_at"]

# Create Genre to GenList (POST)
class CreateGenreListAPIView(generics.CreateAPIView):
    queryset = Genre.objects.all() 
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAdminUser]

# Genre Detail (GET)
class GetGenreDetailAPIVIew(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]

# Genre Update (PATCH)
class UpdateGenreDetailAPIView(generics.UpdateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    permission_classes = [permissions.IsAdminUser]

# Genre Delete (DELETE)
class DeleteGenreDetailAPIView(generics.DeleteAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    permission_classes = [permissions.IsAdminUser]
