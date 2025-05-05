from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# API URLs
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.users.api.urls"), name="users"),
    path("api/v1/genres/", include("apps.genre.api.urls"), name="genres"),
    path("api/v1/artists/", include("apps.artists.api.urls"), name="artists"),
    path("api/v1/tracks/", include("apps.audio.api.urls"), name="tracks"),
    path("api/v1/albums/", include("apps.albums.api.urls"), name="albums"),
    path("api/v1/playlists/", include("apps.playlists.api.urls"), name="playlists"),
]

# Media Assets
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Static Assets
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Schema URLs
urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

