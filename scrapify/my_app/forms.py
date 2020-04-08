from django import forms
from .models import Link


class GetLink(forms.ModelForm):
    link = forms.URLField(max_length=10000)
    link.widget.attrs['placeholder'] = "Enter a link to a product"
    link.widget.attrs['class'] = "form-control"

    class Meta:
        model = Link
        fields = ('link',)
