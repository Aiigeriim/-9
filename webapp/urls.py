from django.urls import path

from webapp.views import PhotoListView, PhotoCreateView, PhotoDetailView

# from webapp.views import PhotoCreateView

app_name = "webapp"

urlpatterns = [
    path('', PhotoListView.as_view(), name="photo_list"),
    path('photo/add/', PhotoCreateView.as_view(), name="photo_add"),
    path('post/<int:pk>/', PhotoDetailView.as_view(), name="photo_view"),
#     path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post_update"),
#     path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post_delete"),
#     path('post/<int:pk>/like/', LikePostView.as_view(), name="post_like"),
]
