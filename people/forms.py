from django import forms

from .models import Person, Group


class PersonModelForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'description'
        ]


class GroupModelForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']