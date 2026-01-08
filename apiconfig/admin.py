from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RecentTransaction, KYC

class KYCInline(admin.TabularInline):  # or admin.StackedInline
    model = KYC
    extra = 1
    fields = ['kyc_status', 'image_url', 'created_at']
    readonly_fields = ['created_at']

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ['email']
    list_display = ('email', 'fullname', 'main', 'profit', 'is_staff', 'is_active', 'is_superuser')
    
    fieldsets = (
        (None, {'fields': ('email', 'password', 'fullname')}),
        ('Financial Info', {'fields': ('main', 'profit')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )
    
    # Add inline for KYC records
    inlines = [KYCInline]

@admin.register(RecentTransaction)
class RecentTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'crypto_type', 'transaction_type', 'transaction_status', 'amount', 'created_at', 'time_since_created')
    list_filter = ('crypto_type', 'transaction_type', 'transaction_status')
    search_fields = ('user__email',)
    readonly_fields = ('created_at',)

admin.site.register(CustomUser, CustomUserAdmin)

