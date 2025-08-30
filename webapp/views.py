from django.db import models
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import PhotoForm
from .models import Picture



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
# class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Picture
#     form_class = PhotoForm
#     template_name = "photos/photo_form.html"
#
#     def test_func(self):
#         return self.get_object().author == self.request.user
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs["user"] = self.request.user
#         return kwargs
#
#
# class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Picture
#     template_name = "photos/photo_confirm_delete.html"
#     success_url = reverse_lazy("photo_list")
#
#     def test_func(self):
#         return self.get_object().author == self.request.user

