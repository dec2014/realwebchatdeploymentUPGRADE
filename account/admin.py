from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from chat.models import Room,Messages



admin.site.register(Room)
admin.site.register(Messages)




class CustomUserAdmin(BaseUserAdmin):
    model = User

    list_display = ('email', 'name', 'role', 'is_staff', 'is_superuser')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    search_fields = ('email',)


admin.site.register(User, CustomUserAdmin)