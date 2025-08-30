from django.contrib.admin import action
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse

from accounts.models import User
from .forms import PhotoForm, AlbumForm
from .models import Picture, Album, FavoritePicture, FavoriteAlbum


#
#
#
#
class PhotoListView(ListView):
    model = Picture
    template_name = "photos/photo_list.html"
    # template_name = "posts/posts_list.html"

    context_object_name = "photos"
    paginate_by = 5
    ordering = ("-created_at",)

    def get_queryset(self):
        return super().get_queryset()

    # model = Picture
    # template_name = "photos/photo_list.html"
    # context_object_name = "photos"
    # paginate_by = 5
    # ordering = ['-created_at']
    #
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     if self.request.user.is_authenticated:
    #         # показываем все публичные + свои приватные
    #         return qs.filter(
    #             models.Q(is_public=True) | models.Q(author=self.request.user)
    #         ).select_related("author", "album")
    #     else:
    #         return qs.filter(is_public=True).select_related("author", "album")



#
class PhotoDetailView(DetailView):
    model = Picture
    template_name = "photos/photo_detail.html"
    context_object_name = "photo"
#
#
class PhotoCreateView(CreateView):

    form_class = PhotoForm
    template_name = "photos/photo_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    # model = Picture
    # form_class = PhotoForm
    # template_name = "photos/photo_create.html"
    #
    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)
    #
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["user"] = self.request.user
    #     return kwargs
#
#
class PhotoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Picture
    form_class = PhotoForm
    template_name = "photos/photo_update.html"
    permission_required = 'webapp.change_post'


    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy("webapp:photo_view", kwargs={"pk": self.object.pk})




    # model = Picture
    # form_class = PhotoForm
    # template_name = "photos/photo_form.html"
    #
    # def test_func(self):
    #     return self.get_object().author == self.request.user
    #
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["user"] = self.request.user
    #     return kwargs
#
#
class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

        model = Picture
        template_name = "photos/photo_delete.html"
        context_object_name = "photo"

        # permission_required = 'webapp.delete_picture'

        def test_func(self):
            obj = self.get_object()
            return self.request.user.has_perm('webapp.delete_picture') or obj.author == self.request.user

        def has_permission(self):
            return self.request.user.has_perm('webapp.delete_picture') or self.request.user == self.get_object().author

        def get_success_url(self):
            return reverse("accounts:profile", kwargs={"pk": self.request.user.pk})




    # model = Picture
    # template_name = "photos/photo_confirm_delete.html"
    # success_url = reverse_lazy("photo_list")
    #
    # def test_func(self):
    #     return self.get_object().author == self.request.user



class AlbumListView(ListView):
    model = Album
    template_name = "albums/album_list.html"
    context_object_name = "albums"


    context_object_name = "albums"
    paginate_by = 5
    ordering = ("-created_at",)

    def get_queryset(self):
        return super().get_queryset()


class AlbumDetailView(DetailView):
    model = Album
    template_name = "albums/album_detail.html"
    context_object_name = "album"
#
#
# class AlbumCreateView(CreateView):
#
#     form_class = AlbumForm
#     template_name = "albums/album_create.html"
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)




class AlbumCreateView(CreateView):
    model = Album
    form_class = AlbumForm
    template_name = "albums/album_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"pk": self.request.user.pk})




class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = "albums/album_delete.html"
    context_object_name = "album"

    permission_required = 'webapp.delete_album'

    def test_func(self):
        obj = self.get_object()
        return self.request.user.has_perm('webapp.delete_album') or obj.author == self.request.user

    def has_permission(self):
        return self.request.user.has_perm('webapp.delete_album') or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.request.user.pk})
#
#
class AlbumUpdateView(PermissionRequiredMixin, UpdateView):
    model = Picture
    form_class = PhotoForm
    template_name = "albums/album_update.html"
    permission_required = 'webapp.change_post'


    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy("webapp:photo_view", kwargs={"pk": self.object.pk})
#
#
#
# class FavoritePicture(View):
#     def get(self, request, *args, pk, **kwargs):
#
#         if not request.user.is_authenticated:
#             return JsonResponse({"error": "Unauthorized"}, status=401)
#         photo = get_object_or_404(Picture, pk=pk)
#         if request.user in photo.like_users.all():
#             post.like_users.remove(request.user)
#             action = "unliked"
#         else:
#             post.like_users.add(request.user)
#             action = "liked"
#
#         return JsonResponse({
#             "likes_count": post.like_users.count(),
#             "action": action
#         })

class FavPicView(View):
    def get(self, request, *args, pk, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        photo = get_object_or_404(Picture, pk=pk)
        user = request.user

        favorite, created = FavoritePicture.objects.get_or_create(user=user, photo=photo)

        if not created:

            favorite.delete()
            action = "removed"
        else:
            action = "added"

        return JsonResponse({
            "action": action
        })

class FavPAlbView(View):
    def get(self, request, *args, pk, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        album = get_object_or_404(Album, pk=pk)
        user = request.user

        favorite, created = FavoriteAlbum.objects.get_or_create(user=user, album=album)

        if not created:

            favorite.delete()
            action = "removed"
        else:
            action = "added"

        return JsonResponse({
            "action": action
        })


