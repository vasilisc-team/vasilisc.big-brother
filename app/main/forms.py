from django import forms
from .models import ImageFace
from .models import Image
from .models import ImageRubbish


class Image(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image",)


class ImageRubbishForm(forms.ModelForm):
    class Meta:
        model = ImageRubbish
        fields = ("image",)


class ImageFaceForm(forms.ModelForm):
    class Meta:
        model = ImageFace
        fields = ("image",)