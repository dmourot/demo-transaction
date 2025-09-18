from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import random
from datetime import datetime, timedelta

from accounts.models import UserProfile, Account, Budget
from transactions.models import Category, Transaction, RecurringTransaction


class Command(BaseCommand):
    help = 'Create sample data for the finance application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=3,
            help='Number of users to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Transaction.objects.all().delete()
            RecurringTransaction.objects.all().delete()
            Budget.objects.all().delete()
            Account.objects.all().delete()
            Category.objects.all().delete()
            UserProfile.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.create_categories()
        self.create_users(options['users'])

        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )

    def create_categories(self):
        """Create sample categories"""
        self.stdout.write('Creating categories...')

        categories_data = [
            # Income categories
            {'name': 'Salary', 'category_type': 'INCOME', 'icon': '💰', 'color': '#4CAF50'},
            {'name': 'Freelance', 'category_type': 'INCOME', 'icon': '💼', 'color': '#2196F3'},
            {'name': 'Investment', 'category_type': 'INCOME', 'icon': '📈', 'color': '#FF9800'},
            {'name': 'Gift', 'category_type': 'INCOME', 'icon': '🎁', 'color': '#E91E63'},

            # Expense categories
            {'name': 'Food & Dining', 'category_type': 'EXPENSE', 'icon': '🍽️', 'color': '#FF5722'},
            {'name': 'Transportation', 'category_type': 'EXPENSE', 'icon': '🚗', 'color': '#607D8B'},
            {'name': 'Shopping', 'category_type': 'EXPENSE', 'icon': '🛍️', 'color': '#9C27B0'},
            {'name': 'Entertainment', 'category_type': 'EXPENSE', 'icon': '🎬', 'color': '#673AB7'},
            {'name': 'Bills & Utilities', 'category_type': 'EXPENSE', 'icon': '📋', 'color': '#795548'},
            {'name': 'Healthcare', 'category_type': 'EXPENSE', 'icon': '🏥', 'color': '#009688'},
            {'name': 'Education', 'category_type': 'EXPENSE', 'icon': '📚', 'color': '#3F51B5'},
            {'name': 'Travel', 'category_type': 'EXPENSE', 'icon': '✈️', 'color': '#00BCD4'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category

        # Create subcategories
        subcategories_data = [
            {'name': 'Restaurants', 'parent': 'Food & Dining'},
            {'name': 'Groceries', 'parent': 'Food & Dining'},
            {'name': 'Coffee & Bars', 'parent': 'Food & Dining'},
            {'name': 'Gas', 'parent': 'Transportation'},
            {'name': 'Public Transport', 'parent': 'Transportation'},
            {'name': 'Uber/Taxi', 'parent': 'Transportation'},
            {'name': 'Clothing', 'parent': 'Shopping'},
            {'name': 'Electronics', 'parent': 'Shopping'},
            {'name': 'Home & Garden', 'parent': 'Shopping'},
            {'name': 'Electricity', 'parent': 'Bills & Utilities'},
            {'name': 'Internet', 'parent': 'Bills & Utilities'},
            {'name': 'Phone', 'parent': 'Bills & Utilities'},
        ]

        for sub_data in subcategories_data:
            parent = categories[sub_data['parent']]
            Category.objects.get_or_create(
                name=sub_data['name'],
                parent=parent,
                defaults={
                    'category_type': parent.category_type,
                    'color': parent.color
                }
            )

        self.stdout.write(f'Created {Category.objects.count()} categories')

    def create_users(self, num_users):
        """Create sample users with accounts and transactions"""
        self.stdout.write(f'Creating {num_users} users...')

        sample_users = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
            {'username': 'sarah_johnson', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Johnson'},
            {'username': 'alex_brown', 'email': 'alex@example.com', 'first_name': 'Alex', 'last_name': 'Brown'},
        ]

        for i in range(min(num_users, len(sample_users))):
            user_data = sample_users[i]
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': True
                }
            )

            if created:
                user.set_password('password123')
                user.save()

            # Create user profile
            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                    'date_of_birth': datetime(
                        random.randint(1980, 2000),
                        random.randint(1, 12),
                        random.randint(1, 28)
                    ).date()
                }
            )

            self.create_accounts_for_user(user)

        self.stdout.write(f'Created {User.objects.filter(is_superuser=False).count()} users')

    def create_accounts_for_user(self, user):
        """Create sample accounts for a user"""
        account_types = [
            ('Checking Account', 'CHECKING', Decimal('2500.00')),
            ('Savings Account', 'SAVINGS', Decimal('15000.00')),
            ('Credit Card', 'CREDIT', Decimal('-850.00')),
        ]

        accounts = []
        for name, acc_type, balance in account_types:
            account = Account.objects.create(
                user=user,
                account_name=f"{user.first_name}'s {name}",
                account_type=acc_type,
                balance=balance,
                initial_balance=balance,
                account_number=f"{random.randint(1000000000, 9999999999)}"
            )
            accounts.append(account)

        self.create_transactions_for_accounts(accounts)
        self.create_budgets_for_user(user)

    def create_transactions_for_accounts(self, accounts):
        """Create sample transactions for accounts"""
        categories = list(Category.objects.all())

        # Sample transaction data
        income_transactions = [
            ('Monthly Salary', 'INCOME', 4500.00, 'Salary'),
            ('Freelance Project', 'INCOME', 1200.00, 'Freelance'),
            ('Stock Dividend', 'INCOME', 150.00, 'Investment'),
        ]

        expense_transactions = [
            ('Whole Foods', 'EXPENSE', 89.50, 'Groceries'),
            ('Starbucks', 'EXPENSE', 4.75, 'Coffee & Bars'),
            ('Shell Gas Station', 'EXPENSE', 45.00, 'Gas'),
            ('Netflix Subscription', 'EXPENSE', 15.99, 'Entertainment'),
            ('Electric Bill', 'EXPENSE', 125.00, 'Electricity'),
            ('Amazon Purchase', 'EXPENSE', 67.99, 'Shopping'),
            ('Uber Ride', 'EXPENSE', 18.50, 'Uber/Taxi'),
            ('Restaurant Dinner', 'EXPENSE', 85.00, 'Restaurants'),
            ('Gym Membership', 'EXPENSE', 50.00, 'Healthcare'),
            ('Movie Tickets', 'EXPENSE', 28.00, 'Entertainment'),
        ]

        for account in accounts:
            # Create income transactions (mainly for checking account)
            if account.account_type in ['CHECKING', 'SAVINGS']:
                for title, trans_type, amount, cat_name in income_transactions:
                    category = None
                    for cat in categories:
                        if cat.name == cat_name:
                            category = cat
                            break

                    # Create monthly income for the last 3 months
                    for month_offset in range(3):
                        date = timezone.now().date() - timedelta(days=30 * month_offset)
                        Transaction.objects.create(
                            account=account,
                            transaction_type=trans_type,
                            title=title,
                            amount=Decimal(str(amount)),
                            category=category,
                            date=date,
                            payment_method='BANK_TRANSFER',
                            created_by=account.user
                        )

            # Create expense transactions for all accounts
            for _ in range(random.randint(15, 30)):
                title, trans_type, amount, cat_name = random.choice(expense_transactions)
                category = None
                for cat in categories:
                    if cat.name == cat_name:
                        category = cat
                        break

                # Random date within last 30 days
                date = timezone.now().date() - timedelta(days=random.randint(1, 30))

                Transaction.objects.create(
                    account=account,
                    transaction_type=trans_type,
                    title=title + f" #{random.randint(1000, 9999)}",
                    amount=Decimal(str(amount * random.uniform(0.5, 1.5))).quantize(Decimal('0.01')),
                    category=category,
                    date=date,
                    payment_method=random.choice(['CREDIT_CARD', 'DEBIT_CARD', 'CASH']),
                    merchant=title.split()[0] if ' ' in title else title,
                    created_by=account.user
                )

    def create_budgets_for_user(self, user):
        """Create sample budgets for a user"""
        expense_categories = Category.objects.filter(category_type__in=['EXPENSE', 'BOTH'])

        budget_data = [
            ('Monthly Food Budget', 'Food & Dining', 500.00),
            ('Transportation Budget', 'Transportation', 200.00),
            ('Entertainment Budget', 'Entertainment', 150.00),
            ('Shopping Budget', 'Shopping', 300.00),
        ]

        for name, cat_name, amount in budget_data:
            category = expense_categories.filter(name=cat_name).first()
            if category:
                Budget.objects.create(
                    user=user,
                    name=name,
                    category=category,
                    amount=Decimal(str(amount)),
                    period='MONTHLY',
                    start_date=timezone.now().date().replace(day=1)
                )