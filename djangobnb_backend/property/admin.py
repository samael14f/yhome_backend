from django.contrib import admin

from .models import *


admin.site.register(Property)
admin.site.register([Reservation, Reviews, Complaints,PropertyVerification])