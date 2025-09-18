from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Account, Budget


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_name', 'account_type', 'balance', 'currency', 'user', 'is_active', 'created_at']
    list_filter = ['account_type', 'currency', 'is_active', 'created_at']
    search_fields = ['account_name', 'user__username', 'user__email', 'account_number']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'account_name', 'account_type', 'account_number')
        }),
        ('Financial Details', {
            'fields': ('balance', 'initial_balance', 'currency')
        }),
        ('Additional Information', {
            'fields': ('description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category', 'amount', 'period', 'get_spent_amount', 'get_percentage_used', 'is_active']
    list_filter = ['period', 'is_active', 'created_at']
    search_fields = ['name', 'user__username', 'category__name']
    readonly_fields = ['created_at', 'updated_at', 'get_spent_amount', 'get_remaining_budget', 'get_percentage_used']
    list_editable = ['is_active']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'category')
        }),
        ('Budget Details', {
            'fields': ('amount', 'period', 'start_date', 'end_date')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Budget Tracking', {
            'fields': ('get_spent_amount', 'get_remaining_budget', 'get_percentage_used'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_spent_amount(self, obj):
        return f"${obj.get_spent_amount():.2f}"
    get_spent_amount.short_description = 'Spent Amount'

    def get_percentage_used(self, obj):
        return f"{obj.get_percentage_used():.1f}%"
    get_percentage_used.short_description = 'Used %'


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
