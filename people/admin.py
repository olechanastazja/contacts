from django.contrib import admin
from .models import (Person,
                     Address,
                     EmailAddress,
                     PhoneNumber,
                     Group)

admin.site.register(Person)
admin.site.register(Address)
admin.site.register(EmailAddress)
admin.site.register(PhoneNumber)
admin.site.register(Group)