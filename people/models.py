from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from group.models import Group


class Person(models.Model):
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    group = models.ManyToManyField(Group)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Address(models.Model):
    city = models.CharField(max_length=100, null=False, blank=False)
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10, null=False, blank=False)
    people = models.ManyToManyField(Person)

    def __str__(self):
        return f'{self.street} {self.street_number} {self.city}'


class PhoneNumber(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="""Phone number must be entered in the format: 
                                                                    '+999999999'. Up to 15 digits allowed.""")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    type = models.CharField(max_length=50)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class EmailAddress(models.Model):
    email = models.EmailField()
    type = models.CharField(max_length=50)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)



