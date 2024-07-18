from django.contrib import admin

from .models import User,StaffMembers

admin.site.register([User,StaffMembers])