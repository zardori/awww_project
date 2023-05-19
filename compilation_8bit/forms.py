from django import forms
from django.forms import ModelForm
from .models import FilesystemItem, File


class AddFileForm(ModelForm):
    class Meta:
        model = File
        fields = ['name', 'content']

    parent_id = forms.IntegerField()
