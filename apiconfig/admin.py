from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ['email']
    # Display in list view
    list_display = ('email', 'fullname', 'main', 'profit',)

    # Show in the form view
    fieldsets = (
        (None, {'fields': ('email', 'password', 'fullname')}),
        ('Financial Info', {'fields': ('main', 'profit',)}),
        ('KYC Info', {'fields': ('kyc_status', 'kyc_photo')}),
    )

    # readonly_fields = ('total',)

    exclude = ('groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login',)

admin.site.register(CustomUser, CustomUserAdmin)

