from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile for additional user information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Account(models.Model):
    """Financial account model - users can have multiple accounts"""

    ACCOUNT_TYPES = [
        ('CHECKING', 'Checking Account'),
        ('SAVINGS', 'Savings Account'),
        ('CREDIT', 'Credit Card'),
        ('INVESTMENT', 'Investment Account'),
        ('LOAN', 'Loan Account'),
        ('CASH', 'Cash'),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('CAD', 'Canadian Dollar'),
        ('AUD', 'Australian Dollar'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='CHECKING')
    account_number = models.CharField(max_length=50, blank=True, help_text="Optional account number for reference")
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('-999999999.99'))]
    )
    initial_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Starting balance when account was created"
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [['user', 'account_name']]
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['account_type']),
        ]

    def __str__(self):
        return f"{self.account_name} ({self.get_account_type_display()}) - {self.user.username}"

    def update_balance(self, amount):
        """Update account balance by amount (positive for credit, negative for debit)"""
        self.balance += Decimal(str(amount))
        self.save(update_fields=['balance', 'updated_at'])

    def get_total_income(self):
        """Calculate total income for this account"""
        from transactions.models import Transaction
        return Transaction.objects.filter(
            account=self,
            transaction_type='INCOME'
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')

    def get_total_expense(self):
        """Calculate total expenses for this account"""
        from transactions.models import Transaction
        return Transaction.objects.filter(
            account=self,
            transaction_type='EXPENSE'
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')

    def get_monthly_summary(self, year, month):
        """Get monthly transaction summary"""
        from transactions.models import Transaction
        transactions = Transaction.objects.filter(
            account=self,
            date__year=year,
            date__month=month
        )

        income = transactions.filter(transaction_type='INCOME').aggregate(
            total=models.Sum('amount'))['total'] or Decimal('0.00')
        expense = transactions.filter(transaction_type='EXPENSE').aggregate(
            total=models.Sum('amount'))['total'] or Decimal('0.00')

        return {
            'income': income,
            'expense': expense,
            'net': income - expense,
            'transaction_count': transactions.count()
        }


class Budget(models.Model):
    """Budget model for tracking spending limits per category"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    name = models.CharField(max_length=100)
    category = models.ForeignKey('transactions.Category', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    period = models.CharField(
        max_length=20,
        choices=[
            ('MONTHLY', 'Monthly'),
            ('WEEKLY', 'Weekly'),
            ('YEARLY', 'Yearly'),
            ('CUSTOM', 'Custom Period'),
        ],
        default='MONTHLY'
    )
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [['user', 'name']]

    def __str__(self):
        return f"{self.name} - {self.amount} ({self.period})"

    def get_spent_amount(self):
        """Calculate amount spent in current budget period"""
        from transactions.models import Transaction
        from datetime import datetime, timedelta

        if self.period == 'MONTHLY':
            start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end = (start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
        elif self.period == 'WEEKLY':
            start = timezone.now() - timedelta(days=timezone.now().weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=7) - timedelta(seconds=1)
        elif self.period == 'YEARLY':
            start = timezone.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = start.replace(year=start.year + 1) - timedelta(seconds=1)
        else:
            start = self.start_date
            end = self.end_date or timezone.now()

        transactions = Transaction.objects.filter(
            account__user=self.user,
            transaction_type='EXPENSE',
            date__range=[start, end]
        )

        if self.category:
            transactions = transactions.filter(category=self.category)

        return transactions.aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')

    def get_remaining_budget(self):
        """Calculate remaining budget"""
        return self.amount - self.get_spent_amount()

    def get_percentage_used(self):
        """Calculate percentage of budget used"""
        spent = self.get_spent_amount()
        if self.amount > 0:
            return min((spent / self.amount) * 100, 100)
        return 0
