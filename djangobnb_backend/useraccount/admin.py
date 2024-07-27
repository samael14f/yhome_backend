from django.contrib import admin

from .models import User,StaffMembers,OTPtoken

admin.site.register([User,StaffMembers,OTPtoken])