from django.urls import path
from webapp.views import PhotoListView, PhotoCreateView, PhotoDetailView, PhotoUpdateView, PhotoDeleteView
app_name = "webapp"

urlpatterns = [
    path('', PhotoListView.as_view(), name="photo_list"),
    path('photo/add/', PhotoCreateView.as_view(), name="photo_add"),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name="photo_view"),
    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name="photo_update"),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name="photo_delete"),
#     path('post/<int:pk>/like/', LikePostView.as_view(), name="post_like"),
]
