from django import forms
from .models import Picture, Album

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ["image", "caption", "album", "is_public"]




    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop("user", None)
    #     super().__init__(*args, **kwargs)
    #     if user:
    #         self.fields["album"].queryset = Album.objects.filter(author=user)
    #
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     album = cleaned_data.get("album")
    #     is_public = cleaned_data.get("is_public")

        # if album and not album.is_public and is_public:
        #     raise forms.ValidationError(
        #         "Фотография не может быть публичной, если альбом приватный."
        #     )
        # return cleaned_data
