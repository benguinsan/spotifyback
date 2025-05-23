from django.urls import path

from . import views

app_name = "albums"

urlpatterns = [
    path("", views.AlbumListAPIView.as_view(), name="album-list"),
    path("my/", views.MyAlbumListCreateAPIView.as_view(), name="my-album-list-create"),
    path("my/<slug:slug>/", views.MyAlbumDetailAPIView.as_view(), name="my-album-detail"),
    
    path("favorite/", views.AlbumFavoriteListAPIView.as_view(), name="album-favorite"),
    path("<slug:slug>/", views.AlbumDetailAPIView.as_view(), name="album-detail"),
    path("<slug:slug>/favorite/", views.AlbumFavoriteCreateAPIView.as_view(), name="album-favorite-create-delete"),
]