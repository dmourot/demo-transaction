# API Usage Guide

## Quick Start

### 1. Start the Server
```bash
# Activate virtual environment
source venv/bin/activate

# Start Django development server
python manage.py runserver
```

### 2. Access the API
- **Interactive Documentation:** http://localhost:8000/api/v1/docs
- **Swagger UI:** http://localhost:8000/api/v1/swagger
- **ReDoc:** http://localhost:8000/api/v1/redoc

### 3. Test the API
```bash
# Run the test script
python test_api.py
```

## Available Endpoints

### Accounts
- `GET /api/v1/accounts/` - List all accounts (with pagination and filtering)
- `GET /api/v1/accounts/{id}/` - Get specific account
- `GET /api/v1/accounts/{id}/summary/` - Get account summary with totals
- `GET /api/v1/accounts/statistics/` - Get accounts statistics

### User Profiles
- `GET /api/v1/user-profiles/` - List all user profiles
- `GET /api/v1/user-profiles/{id}/` - Get specific user profile

### Budgets
- `GET /api/v1/budgets/` - List all budgets
- `GET /api/v1/budgets/{id}/` - Get specific budget

## Example Usage

### Using curl
```bash
# List accounts (requires authentication)
curl -X GET "http://localhost:8000/api/v1/accounts/" \
  -H "Cookie: sessionid=your_session_id"

# Get account details
curl -X GET "http://localhost:8000/api/v1/accounts/1/" \
  -H "Cookie: sessionid=your_session_id"

# Filter accounts by type
curl -X GET "http://localhost:8000/api/v1/accounts/?account_type=CHECKING" \
  -H "Cookie:sessionid=your_session_id"
```

### Using Python requests
```python
import requests

# Create session for authentication
session = requests.Session()

# Login first (you need to implement this based on your auth setup)
# session.post('http://localhost:8000/admin/login/', data={'username': 'user', 'password': 'pass'})

# Get accounts
response = session.get('http://localhost:8000/api/v1/accounts/')
accounts = response.json()

print(f"Found {len(accounts['accounts'])} accounts")
```

## Authentication

The API uses Django's built-in authentication system. You need to be logged in to access the endpoints. You can:

1. **Use the Django admin interface** to log in first
2. **Use session-based authentication** with cookies
3. **Implement token-based authentication** if needed

## Filtering and Pagination

All list endpoints support:
- **Pagination:** `?page=1&page_size=20`
- **Search:** `?search=checking`
- **Filtering:** Various filters depending on the endpoint

See the full documentation in `API_DOCUMENTATION.md` for complete details.
