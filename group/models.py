from django.db import models
from people.models import Person
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=100)
    people = models.ManyToManyField(Person)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
