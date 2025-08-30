from django.http import request
from django.urls import path

from webapp.views import PhotoListView, PhotoCreateView, PhotoDetailView, PhotoUpdateView, PhotoDeleteView, \
    AlbumListView, AlbumDetailView, AlbumUpdateView, AlbumDeleteView, AlbumCreateView, FavPicView

app_name = "webapp"

urlpatterns = [
    path('', PhotoListView.as_view(), name="photo_list"),
    path('photo/add/', PhotoCreateView.as_view(), name="photo_add"),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name="photo_view"),
    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name="photo_update"),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name="photo_delete"),

    path('photo/<int:pk>/favorite/', FavPicView.as_view(), name="post_like"),
    path('album/<int:pk>/favorite/', FavPicView.as_view(), name="alb_fav"),

    path('albums/', AlbumListView.as_view(), name="album_list"),
    path('album/add/', AlbumCreateView.as_view(), name="album_add"),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name="album_view"),
    path('album/<int:pk>/update/', AlbumUpdateView.as_view(), name="album_update"),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name="album_delete"),
]
