from django import forms
from .models import Link


class GetLink(forms.ModelForm):
    link = forms.URLField(max_length=10000)
    link.widget.attrs['placeholder'] = "Enter product's URL to analyze"
    link.widget.attrs['class'] = "form-control"
    link.widget.attrs['id'] = "link"
    link.widget.attrs['name'] = "link"

    class Meta:
        model = Link
        fields = ('link',)
