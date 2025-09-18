from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
from accounts.models import Account


class Category(models.Model):
    """Category model for organizing transactions"""

    CATEGORY_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
        ('BOTH', 'Both'),
    ]

    name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES, default='BOTH')
    icon = models.CharField(max_length=50, blank=True, help_text="Icon name or emoji for UI display")
    color = models.CharField(max_length=7, blank=True, help_text="Hex color code for UI display")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
        unique_together = [['name', 'parent']]

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def get_full_path(self):
        """Get full category path including parent categories"""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name


class Transaction(models.Model):
    """Transaction model for recording financial transactions"""

    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
        ('TRANSFER', 'Transfer'),
    ]

    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CHECK', 'Check'),
        ('MOBILE_PAY', 'Mobile Payment'),
        ('OTHER', 'Other'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='CASH')

    # For transfers
    to_account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incoming_transfers',
        help_text="Target account for transfers"
    )

    # Additional fields
    merchant = models.CharField(max_length=100, blank=True, help_text="Store or merchant name")
    location = models.CharField(max_length=200, blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    receipt_image = models.ImageField(upload_to='receipts/', null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True, help_text="Whether transaction has been verified/reconciled")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_transactions')

    class Meta:
        ordering = ['-date', '-time']
        indexes = [
            models.Index(fields=['account', 'date']),
            models.Index(fields=['transaction_type', 'date']),
            models.Index(fields=['category', 'date']),
        ]

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.transaction_type})"

    def save(self, *args, **kwargs):
        """Override save to update account balance"""
        is_new = self.pk is None
        old_amount = None
        old_type = None

        if not is_new:
            # Get old values if updating
            old_transaction = Transaction.objects.get(pk=self.pk)
            old_amount = old_transaction.amount
            old_type = old_transaction.transaction_type

        super().save(*args, **kwargs)

        # Update account balance
        if is_new:
            if self.transaction_type == 'INCOME':
                self.account.update_balance(self.amount)
            elif self.transaction_type == 'EXPENSE':
                self.account.update_balance(-self.amount)
            elif self.transaction_type == 'TRANSFER' and self.to_account:
                self.account.update_balance(-self.amount)
                self.to_account.update_balance(self.amount)
        else:
            # Handle updates
            if old_type == 'INCOME':
                self.account.update_balance(-old_amount)
            elif old_type == 'EXPENSE':
                self.account.update_balance(old_amount)

            if self.transaction_type == 'INCOME':
                self.account.update_balance(self.amount)
            elif self.transaction_type == 'EXPENSE':
                self.account.update_balance(-self.amount)

    def delete(self, *args, **kwargs):
        """Override delete to update account balance"""
        if self.transaction_type == 'INCOME':
            self.account.update_balance(-self.amount)
        elif self.transaction_type == 'EXPENSE':
            self.account.update_balance(self.amount)
        elif self.transaction_type == 'TRANSFER' and self.to_account:
            self.account.update_balance(self.amount)
            self.to_account.update_balance(-self.amount)

        super().delete(*args, **kwargs)

    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class RecurringTransaction(models.Model):
    """Model for setting up recurring transactions"""

    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('BIWEEKLY', 'Bi-weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('YEARLY', 'Yearly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='recurring_transactions')
    transaction_type = models.CharField(max_length=10, choices=Transaction.TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    next_due_date = models.DateField()
    is_active = models.BooleanField(default=True)
    auto_create = models.BooleanField(default=False, help_text="Automatically create transactions")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['next_due_date']

    def __str__(self):
        return f"{self.title} - {self.frequency} ({self.amount})"

    def create_transaction(self):
        """Create a transaction from this recurring template"""
        transaction = Transaction.objects.create(
            account=self.account,
            transaction_type=self.transaction_type,
            category=self.category,
            amount=self.amount,
            title=self.title,
            description=self.description,
            date=self.next_due_date,
            is_recurring=True,
            created_by=self.user
        )

        # Update next due date
        from datetime import timedelta
        if self.frequency == 'DAILY':
            self.next_due_date += timedelta(days=1)
        elif self.frequency == 'WEEKLY':
            self.next_due_date += timedelta(weeks=1)
        elif self.frequency == 'BIWEEKLY':
            self.next_due_date += timedelta(weeks=2)
        elif self.frequency == 'MONTHLY':
            # Handle month-end dates properly
            from dateutil.relativedelta import relativedelta
            self.next_due_date += relativedelta(months=1)
        elif self.frequency == 'QUARTERLY':
            from dateutil.relativedelta import relativedelta
            self.next_due_date += relativedelta(months=3)
        elif self.frequency == 'YEARLY':
            from dateutil.relativedelta import relativedelta
            self.next_due_date += relativedelta(years=1)

        self.save()
        return transaction
