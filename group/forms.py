from django import forms
from .models import Group


class GroupModelForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']