from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.core import pagination
from apps.genre.api.serializers import GenreSerializer
from apps.genre.models import Genre

# Get, Post List Genre (GET, POST)
class GenreListAPIView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = pagination.MaxResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["created_at"]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

# Get, Put, Delete Genre (GET, PUT, DELETE)
class GenreDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()