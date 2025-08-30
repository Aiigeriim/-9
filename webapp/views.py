from django.db import models
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from .forms import PhotoForm
from .models import Picture, Album


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
    # template_name = "photos/photo_form.html"
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
    paginate_by = 5
    ordering = ("-created_at",)

    def get_queryset(self):
        return super().get_queryset()

