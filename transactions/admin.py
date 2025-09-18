from django.contrib import admin
from .models import Category, Transaction, RecurringTransaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'parent', 'get_full_path', 'is_active', 'created_at']
    list_filter = ['category_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at', 'get_full_path']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category_type', 'parent')
        }),
        ('Display Settings', {
            'fields': ('icon', 'color', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Calculated Fields', {
            'fields': ('get_full_path',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['title', 'account', 'transaction_type', 'amount', 'category', 'date', 'payment_method', 'is_verified']
    list_filter = ['transaction_type', 'payment_method', 'is_verified', 'is_recurring', 'date', 'account__account_type']
    search_fields = ['title', 'description', 'merchant', 'account__account_name', 'account__user__username']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_verified']

    fieldsets = (
        ('Basic Information', {
            'fields': ('account', 'transaction_type', 'title', 'amount')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Date & Time', {
            'fields': ('date', 'time')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'merchant', 'location')
        }),
        ('Transfer Details', {
            'fields': ('to_account',),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('description', 'receipt_image')
        }),
        ('Status', {
            'fields': ('is_verified', 'is_recurring')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('account', 'category', 'to_account', 'created_by')


@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'account', 'transaction_type', 'amount', 'frequency', 'next_due_date', 'is_active', 'auto_create']
    list_filter = ['transaction_type', 'frequency', 'is_active', 'auto_create', 'account__account_type']
    search_fields = ['title', 'description', 'user__username', 'account__account_name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active', 'auto_create']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'account', 'transaction_type', 'title', 'amount')
        }),
        ('Categorization', {
            'fields': ('category',)
        }),
        ('Schedule', {
            'fields': ('frequency', 'start_date', 'end_date', 'next_due_date')
        }),
        ('Settings', {
            'fields': ('is_active', 'auto_create')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['create_transactions_now']

    def create_transactions_now(self, request, queryset):
        count = 0
        for recurring_transaction in queryset.filter(is_active=True):
            recurring_transaction.create_transaction()
            count += 1
        self.message_user(request, f'Created {count} transactions.')
    create_transactions_now.short_description = 'Create transactions now'
