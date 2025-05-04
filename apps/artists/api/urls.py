from django.urls import path

from . import views

app_name = "artists"

urlpatterns = [
    # Artists
    path("", views.ArtistListCreateAPIView.as_view(), name="artist-list"),
    path("me/", views.ArtistDetailMeAPIView.as_view(), name="artist-me"),
    path("me/image/", views.MyArtistImageAPIView.as_view(), name="artist-image"),
    path("me/verify/", views.ArtistVerifyMeAPIView.as_view(), name="artist-verify"),
    path("favorites/", views.ArtistFavoriteListAPIView.as_view(), name="artist-favorite-list"),
    path("<slug:slug>/", views.ArtistDetailAPIView.as_view(), name="artist-detail"),
    path("<slug:slug>/favorite/", views.ArtistFavoriteCreateAPIView.as_view(), name="artist-favorite"),
]