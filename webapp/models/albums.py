from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="albums",
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_public = models.BooleanField(default=True, verbose_name="Публичный альбом")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "albums"
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"