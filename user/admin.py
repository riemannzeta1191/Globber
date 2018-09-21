from django.contrib import admin
from .models import GlobberUser
from django.contrib.auth.admin import UserAdmin





admin.site.register(GlobberUser, UserAdmin)