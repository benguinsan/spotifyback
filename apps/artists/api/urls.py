from django.urls import path

from . import views

app_name = "artists"

urlpatterns = [
    path("", views.GetArtistListAPIView.as_view(), name="artist-list"),
    path("create/", views.CreateArtistAPIView.as_view(), name="artist-create"),
    path("detail/<slug:slug>/", views.GetDetailArtistAPIView.as_view(), name="artist-detail"),
    path("me/", views.GetDetailArtistAPIView.as_view(), name="artist-me"),
    path("favorite/", views.GetArtistFavoriteListAPIView.as_view(), name="artist-favorite"),
    path("favorite/create/", views.ArtistFavoriteCreateAPIView.as_view(), name="artist-favorite-create"),
    path("favorite/delete/", views.ArtistFavoriteDeleteAPIView.as_view(), name="artist-favorite-delete"),
]