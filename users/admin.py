from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

from django.utils.translation import ugettext_lazy as _


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('phone_number', 'confirmation_code')}),
        (_('Personal info'), {'fields': ('inviter_code',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    ordering = ('phone_number',)
    list_display = (
        'pk',
        'phone_number',
        'confirmation_code',
        'my_invite_code',
        'inviter_code')


admin.site.register(User, CustomUserAdmin)
