from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Credential

class UsersAdmin(admin.ModelAdmin):
    pass

admin.site.register(Credential, UsersAdmin)
admin.site.unregister(Group)