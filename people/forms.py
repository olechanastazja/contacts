from django import forms

from .models import Person, Address, PhoneNumber, EmailAddress
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
        self.fields['description'].widget.attrs['rows'] = 4


class AddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'city', 'street', 'street_number'
        ]


class PhoneModelForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = [
            'phone_number', 'type'
        ]


class EmailModelForm(forms.ModelForm):
    class Meta:
        model = EmailAddress
        fields = [
            'email', 'type'
        ]
