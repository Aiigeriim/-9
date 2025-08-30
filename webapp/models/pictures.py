from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


from webapp.models import Album


class Picture(models.Model):
    image = models.ImageField(upload_to="photos/", verbose_name="Фотография")
    caption = models.CharField(max_length=100, verbose_name="Подпись")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="Автор"
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        related_name="photos",
        null=True,
        blank=True,
        verbose_name="Альбом"
    )
    is_public = models.BooleanField(default=True, verbose_name="Публичная фотография")
    # token = models.CharField(max_length=64, blank=True, null=True, unique=True)

    def __str__(self):
        return self.caption


    def get_absolute_url(self):
        return reverse("webapp:photo_view", kwargs={"pk": self.pk})

    class Meta:
        db_table = "pictures"
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"