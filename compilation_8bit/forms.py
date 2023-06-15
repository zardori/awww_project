#
#
# from django import forms
# from django.forms import ModelForm
# from .models import FilesystemItem, File
#
#
# class AddFileForm(ModelForm):
#     class Meta:
#         model = File
#         fields = ['name', 'content']
#
#     parent_id = forms.IntegerField()
#
#
# class DelObjectForm(forms.Form):
#
#     object_id = forms.IntegerField()
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         model = kwargs.pop('model', None)
#         # If the user is not specified the form is created in wrong way.
#         assert(user is not None)
#         assert(model is not None)
#
#         self.user = user
#         self.model = model
#
#         super(DelObjectForm, self).__init__(*args, **kwargs)
#
#
#
#     def clean_object_id(self):
#         cleaned_id = self.cleaned_data['object_id']




