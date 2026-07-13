from django import forms
from .models import GalleryItem


class GalleryItemForm(forms.ModelForm):
    image_r2_key = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = GalleryItem
        fields = ['image']