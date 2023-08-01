from django.contrib import admin
from core.models import Car, Booking, Review, Payment
from django.contrib.auth.models import Group


admin.site.register([Car, Booking, Review, Payment])
admin.site.unregister(Group)
