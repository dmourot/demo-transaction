# Accounts API Documentation

## Overview
This is a read-only API for retrieving account data, user profiles, and budget information from the demo-transaction Django application.

**Base URL:** `http://localhost:8000/api/v1/`

## Authentication
All endpoints require Django authentication. You need to be logged in to access the API endpoints.

## Available Endpoints

### 1. Accounts

#### List Accounts
- **GET** `/accounts/`
- **Description:** Retrieve a paginated list of all accounts with optional filtering
- **Authentication:** Required
- **Query Parameters:**
  - `page` (int, optional): Page number (default: 1, min: 1)
  - `page_size` (int, optional): Items per page (default: 20, min: 1, max: 100)
  - `account_type` (string, optional): Filter by account type (CHECKING, SAVINGS, CREDIT, INVESTMENT, LOAN, CASH)
  - `currency` (string, optional): Filter by currency (USD, EUR, GBP, JPY, CAD, AUD)
  - `is_active` (boolean, optional): Filter by active status
  - `search` (string, optional): Search in account name and description
  - `user_id` (int, optional): Filter by user ID

**Example Request:**
```bash
GET /api/v1/accounts/?page=1&page_size=10&account_type=CHECKING&is_active=true
```

**Response:**
```json
{
  "accounts": [
    {
      "id": 1,
      "user_id": 1,
      "username": "john_doe",
      "account_name": "Main Checking",
      "account_type": "CHECKING",
      "account_type_display": "Checking Account",
      "account_number": "1234567890",
      "balance": "1500.00",
      "initial_balance": "1000.00",
      "currency": "USD",
      "currency_display": "US Dollar",
      "description": "Primary checking account",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-20T14:22:00Z"
    }
  ],
  "total_count": 25,
  "page": 1,
  "page_size": 10,
  "total_pages": 3
}
```

#### Get Account Details
- **GET** `/accounts/{account_id}/`
- **Description:** Retrieve details of a specific account
- **Authentication:** Required
- **Path Parameters:**
  - `account_id` (int): Account ID

**Example Request:**
```bash
GET /api/v1/accounts/1/
```

#### Get Account Summary
- **GET** `/accounts/{account_id}/summary/`
- **Description:** Get account summary with income/expense totals
- **Authentication:** Required
- **Path Parameters:**
  - `account_id` (int): Account ID

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "username": "john_doe",
  "account_name": "Main Checking",
  "account_type": "CHECKING",
  "account_type_display": "Checking Account",
  "balance": "1500.00",
  "currency": "USD",
  "currency_display": "US Dollar",
  "is_active": true,
  "total_income": "2500.00",
  "total_expense": "1000.00",
  "net_balance": "3000.00",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 2. User Profiles

#### List User Profiles
- **GET** `/user-profiles/`
- **Description:** Retrieve a paginated list of all user profiles
- **Authentication:** Required
- **Query Parameters:**
  - `page` (int, optional): Page number (default: 1, min: 1)
  - `page_size` (int, optional): Items per page (default: 20, min: 1, max: 100)
  - `user_id` (int, optional): Filter by user ID
  - `search` (string, optional): Search in username

**Example Request:**
```bash
GET /api/v1/user-profiles/?page=1&page_size=5
```

**Response:**
```json
{
  "profiles": [
    {
      "id": 1,
      "user_id": 1,
      "username": "john_doe",
      "phone_number": "+1234567890",
      "date_of_birth": "1990-05-15",
      "address": "123 Main St, City, State 12345",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-20T14:22:00Z"
    }
  ],
  "total_count": 10,
  "page": 1,
  "page_size": 5,
  "total_pages": 2
}
```

#### Get User Profile Details
- **GET** `/user-profiles/{profile_id}/`
- **Description:** Retrieve details of a specific user profile
- **Authentication:** Required
- **Path Parameters:**
  - `profile_id` (int): Profile ID

### 3. Budgets

#### List Budgets
- **GET** `/budgets/`
- **Description:** Retrieve a paginated list of all budgets
- **Authentication:** Required
- **Query Parameters:**
  - `page` (int, optional): Page number (default: 1, min: 1)
  - `page_size` (int, optional): Items per page (default: 20, min: 1, max: 100)
  - `user_id` (int, optional): Filter by user ID
  - `period` (string, optional): Filter by budget period (MONTHLY, WEEKLY, YEARLY, CUSTOM)
  - `is_active` (boolean, optional): Filter by active status
  - `search` (string, optional): Search in budget name

**Example Request:**
```bash
GET /api/v1/budgets/?period=MONTHLY&is_active=true
```

**Response:**
```json
{
  "budgets": [
    {
      "id": 1,
      "user_id": 1,
      "username": "john_doe",
      "name": "Monthly Groceries",
      "category_id": 5,
      "category_name": "Food & Dining",
      "amount": "500.00",
      "period": "MONTHLY",
      "period_display": "Monthly",
      "start_date": "2024-01-01",
      "end_date": null,
      "is_active": true,
      "spent_amount": "350.00",
      "remaining_budget": "150.00",
      "percentage_used": 70.0,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-20T14:22:00Z"
    }
  ],
  "total_count": 8,
  "page": 1,
  "page_size": 20,
  "total_pages": 1
}
```

#### Get Budget Details
- **GET** `/budgets/{budget_id}/`
- **Description:** Retrieve details of a specific budget
- **Authentication:** Required
- **Path Parameters:**
  - `budget_id` (int): Budget ID

### 4. Statistics

#### Get Accounts Statistics
- **GET** `/accounts/statistics/`
- **Description:** Get general statistics about accounts
- **Authentication:** Required

**Response:**
```json
{
  "total_accounts": 25,
  "active_accounts": 23,
  "inactive_accounts": 2,
  "account_types": [
    {"account_type": "CHECKING", "count": 10},
    {"account_type": "SAVINGS", "count": 8},
    {"account_type": "CREDIT", "count": 5},
    {"account_type": "INVESTMENT", "count": 2}
  ],
  "currencies": [
    {"currency": "USD", "count": 20},
    {"currency": "EUR", "count": 3},
    {"currency": "GBP", "count": 2}
  ],
  "balance_by_currency": [
    {"currency": "USD", "total_balance": "45000.00"},
    {"currency": "EUR", "total_balance": "5000.00"},
    {"currency": "GBP", "total_balance": "2000.00"}
  ]
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

## Interactive Documentation

The API includes interactive documentation that you can access at:
- **Swagger UI:** `http://localhost:8000/api/v1/swagger`
- **ReDoc:** `http://localhost:8000/api/v1/redoc`

## Testing the API

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. Access the interactive documentation at `http://localhost:8000/api/v1/docs`

3. Use the test script:
   ```bash
   python test_api.py
   ```

## Data Models

### Account Types
- `CHECKING` - Checking Account
- `SAVINGS` - Savings Account
- `CREDIT` - Credit Card
- `INVESTMENT` - Investment Account
- `LOAN` - Loan Account
- `CASH` - Cash

### Currencies
- `USD` - US Dollar
- `EUR` - Euro
- `GBP` - British Pound
- `JPY` - Japanese Yen
- `CAD` - Canadian Dollar
- `AUD` - Australian Dollar

### Budget Periods
- `MONTHLY` - Monthly
- `WEEKLY` - Weekly
- `YEARLY` - Yearly
- `CUSTOM` - Custom Period
