# Finance App Data Model

## Overview

This Django application provides a comprehensive finance management system with support for multiple users, accounts, transactions, and budgeting features.

## Core Models

### 1. User & UserProfile

- **User**: Django's built-in User model
- **UserProfile**: Extended user information
  - Phone number, date of birth, address
  - One-to-one relationship with User

### 2. Account Model

Users can have multiple financial accounts:

- **Account Types**: Checking, Savings, Credit Card, Investment, Loan, Cash
- **Features**:
  - Balance tracking (supports negative balances for credit cards)
  - Initial balance recording
  - Multi-currency support (USD, EUR, GBP, JPY, CAD, AUD)
  - Account status (active/inactive)
  - Unique account names per user

### 3. Transaction Model

Comprehensive transaction tracking:

- **Transaction Types**: Income, Expense, Transfer
- **Features**:
  - Automatic balance updates
  - Category assignment
  - Payment method tracking
  - Merchant and location information
  - Receipt image upload
  - Tag system for flexible organization
  - Recurring transaction support
  - Transfer between accounts

### 4. Category Model

Hierarchical categorization system:

- **Types**: Income, Expense, or Both
- **Features**:
  - Parent/child relationships (subcategories)
  - Icon and color for UI display
  - Full path calculation for nested categories

### 5. Budget Model

Budget tracking and monitoring:

- **Periods**: Monthly, Weekly, Yearly, Custom
- **Features**:
  - Category-based budgets
  - Automatic spending calculation
  - Percentage tracking
  - Active/inactive status

### 6. RecurringTransaction Model

Automated recurring transactions:

- **Frequencies**: Daily, Weekly, Bi-weekly, Monthly, Quarterly, Yearly
- **Features**:
  - Template-based transaction creation
  - Next due date calculation
  - Auto-creation option
  - Date range support

## Key Features

### Balance Management
- Automatic balance updates on transaction create/update/delete
- Support for transfers between accounts
- Negative balance support for credit accounts

### Categorization
- Hierarchical categories with subcategories
- Visual indicators (icons and colors)
- Flexible assignment to income/expense/both

### Reporting & Analytics
- Monthly summaries per account
- Budget tracking with spending analysis
- Transaction filtering by date, category, type
- User-specific data isolation

### Data Integrity
- Unique constraints (account names per user, budget names per user)
- Validation (minimum amounts, required fields)
- Indexes for performance (user+active accounts, transaction dates)

## Sample Data

The application includes a management command to create sample data:

```bash
python manage.py create_sample_data --users 3 --clear
```

This creates:
- 24 predefined categories with subcategories
- 3 sample users with profiles
- Multiple accounts per user (checking, savings, credit)
- Realistic transaction history (3 months of data)
- Sample budgets for each user

## Admin Interface

Comprehensive Django admin interface with:
- Custom list displays and filters
- Fieldset organization
- Inline editing capabilities
- Bulk actions for recurring transactions
- Search functionality across related fields

## API Ready Structure

The models are designed to be API-friendly with:
- Clean serialization support
- Logical field groupings
- Computed properties for dashboard metrics
- Efficient querying with select_related optimization

## Educational Features

Perfect for learning:
- Django model relationships (ForeignKey, OneToOne)
- Custom model methods and properties
- Admin customization
- Data validation
- Signal-like behavior (save/delete overrides)
- Management commands
- Sample data generation

## Security Considerations

- User data isolation (all user-related queries filter by user)
- No sensitive financial data exposure
- Proper permission handling in admin
- Safe decimal handling for monetary values