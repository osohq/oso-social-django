from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Post, Role, Permission

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Role)
admin.site.register(Permission)
