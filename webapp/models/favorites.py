from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from webapp.models import Picture, Album


class FavoriteAlbum(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorite_albums")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="favorited_alb_by")

    class Meta:
        unique_together = ("user", "album")


class FavoritePicture(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="favorite_photos")
    photo = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name="favorited_pic_by")

    class Meta:
        unique_together = ("user", "photo")