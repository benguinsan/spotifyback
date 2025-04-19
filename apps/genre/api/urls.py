from django.urls import path

from . import views

app_name = "other"

urlpatterns = [
    path("genres/", views.GetGenreListAPIView.as_view(), name="genre-list"),
    path("genres/create", views.CreateGenreListAPIView.as_view(), name="genre-create"),
    path("genres/<slug:slug>/", views.GetGenreDetailAPIView.as_view(), name="genre-detail-get"),
    path("genres/update/<slug:slug>/", views.UpdateGenreDetailAPIView.as_view(), name="genre-detail-update"),
    path("genres/delete/<slug:slug>/", views.DeleteGenreDetailAPIView.as_view(), name="genre-detail-delete"),
]