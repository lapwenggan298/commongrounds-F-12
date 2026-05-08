from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile, Role
# Register your models here.

class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    filter_horizontal = ('roles',)


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInLine]


class RoleAdmin(admin.ModelAdmin):
    model = Role
    list_display = ('name', 'display_name')


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'display_name', 'email_address',)
    list_filter = ('roles',)
    search_fields = ('user__username', 'display_name',)
    filter_horizontal = ('roles',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role, RoleAdmin)