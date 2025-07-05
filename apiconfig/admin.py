from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RecentTransaction
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

@admin.register(RecentTransaction)
class RecentTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'crypto_type', 'transaction_type', 'transaction_status', 'amount', 'created_at', 'time_since_created')
    list_filter = ('crypto_type', 'transaction_type', 'transaction_status')
    search_fields = ('user__email',)
    readonly_fields = ('created_at',)

admin.site.register(CustomUser, CustomUserAdmin)

