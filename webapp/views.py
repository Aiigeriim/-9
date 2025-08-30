from secrets import token_urlsafe

from django.contrib.admin import action
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse


from .forms import PhotoForm, AlbumForm
from .models import Picture, Album, FavoritePicture, FavoriteAlbum


class PhotoListView(ListView):
    model = Picture
    template_name = "photos/photo_list.html"
    # template_name = "posts/posts_list.html"

    context_object_name = "photos"
    paginate_by = 5
    ordering = ("-created_at",)

    def get_queryset(self):
        return super().get_queryset()



#
class PhotoDetailView(DetailView):
    model = Picture
    template_name = "photos/photo_detail.html"
    context_object_name = "photo"

class PhotoTokenView(DetailView):
    model = Picture
    template_name = "photos/photo_detail.html"
    slug_field = 'access_token'
    slug_url_kwarg = 'token'

    def get_queryset(self):
        return Picture.objects.all()
#
#
class PhotoCreateView(CreateView):

    form_class = PhotoForm
    template_name = "photos/photo_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PhotoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Picture
    form_class = PhotoForm
    template_name = "photos/photo_update.html"
    permission_required = 'webapp.change_post'


    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy("webapp:photo_view", kwargs={"pk": self.object.pk})





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




class AlbumListView(ListView):
    model = Album
    template_name = "albums/album_list.html"
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

class GenerateTokenView(View):
    def post(self, request, pk):
        photo = get_object_or_404(Picture, pk=pk, author=request.user)
        if not photo.access_token:
            photo.access_token = token_urlsafe(16)
            photo.save()
        return redirect(reverse("webapp:photo_view", kwargs={"pk": photo.pk}))

