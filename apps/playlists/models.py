import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel
from apps.genre.models import Genre
from apps.audio.models import Track
from apps.core.services import generate_color_from_image, get_path_upload_image_playlist, validate_image_size

User = get_user_model()

# Create your models here.
class Playlist(TimeStampedModel):

    # Playlsit Model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    tracks = models.ManyToManyField(Track, related_name="playlists")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name="playlists")
    title = models.CharField(_("title"), max_length=255, blank=True)
    description = models.TextField(_("description"), blank=True, max_length=500)
    slug = AutoSlugField(populate_from="title", unique=True)
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=get_path_upload_image_playlist,
        validators=[validate_image_size],
        blank=True,
        default="default/playlist.jpg",
    )
    release_date = models.DateField(_("release date"), blank=True, null=True, 
        # default=date.today
    )
    is_private = models.BooleanField(_("is_private"), default=False)

    class Meta:
        verbose_name = _("Playlist")
        verbose_name_plural = _("Playlists")
        ordering = ["-updated_at", "-created_at"]


class FavoritePlaylist(TimeStampedModel):

    # FavoritePlaylist
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_playlists")
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="favorite_playlists")

    class Meta:
        verbose_name = _("Favorite playlist")
        verbose_name_plural = _("Favorite playlists")
        unique_together = ("user", "playlist")
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return f"{self.user} is favorite {self.playlist.title}"