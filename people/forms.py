from django import forms

from .models import Person
from group.forms import Group


class PersonModelForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'description', 'group'
        ]

    def __init__(self, user, *args, **kwargs):
        super(PersonModelForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(user=user)
