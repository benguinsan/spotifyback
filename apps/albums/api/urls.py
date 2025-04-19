from django.urls import path

from . import views

app_name = "albums"

urlpatterns = [
    path("", views.GetAlbumListAPIView.as_view(), name="album-list"),
    path("my/", views.GetMyAlbumListAPIView.as_view(), name="my-album-list"),
    path("my/create/", views.CreateMyAlbumAPIView.as_view(), name="my-album-create"),

    path("my/<slug:slug>/", views.GetMyAlbumDetailAPIView.as_view(), name="my-album-detail"),
    path("my/<slug:slug>/update/", views.UpdateMyAlbumDetailAPIView.as_view(), name="my-album-detail-update"),
    path("my/<slug:slug>/delete/", views.DeleteMyAlbumDetailAPIView.as_view(), name="my-album-detail-delete"),

    path("favorite/", views.GetAlbumFavoriteListAPIView.as_view(), name="album-favorite"),
    path("<slug:slug>/", views.GetAlbumDetailAPIView.as_view(), name="album-detail"),
    path("<slug:slug>/favorite/create/", views.AlbumFavoriteCreateAPIView.as_view(), name="album-favorite-create"),
    path("<slug:slug>/favorite/delete/", views.AlbumFavoriteDeleteAPIView.as_view(), name="album-favorite-delete"),
]