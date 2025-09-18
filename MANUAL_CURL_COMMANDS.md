# Manual CURL Commands for Testing the API

## Quick Reference

### 1. Basic Commands (Without Authentication - Will Return 401)

```bash
# Test basic connectivity
curl -X GET "http://localhost:8000/api/v1/accounts/" -w "\nHTTP Status: %{http_code}\n"

# Test with JSON header
curl -X GET "http://localhost:8000/api/v1/accounts/" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n"

# Test pagination
curl -X GET "http://localhost:8000/api/v1/accounts/?page=1&page_size=5" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n"
```

### 2. Get Session Cookie (Manual Method)

1. **Login via browser:**
   - Go to http://localhost:8000/admin/
   - Login with your Django superuser credentials
   - Open Developer Tools (F12) → Application/Storage → Cookies
   - Copy the `sessionid` value

2. **Use the session cookie:**
```bash
# Replace YOUR_SESSION_ID with the actual session ID
curl -X GET "http://localhost:8000/api/v1/accounts/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"
```

### 3. Complete API Test Commands

#### Accounts Endpoints
```bash
# List all accounts
curl -X GET "http://localhost:8000/api/v1/accounts/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# List with pagination
curl -X GET "http://localhost:8000/api/v1/accounts/?page=1&page_size=10" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Filter by account type
curl -X GET "http://localhost:8000/api/v1/accounts/?account_type=CHECKING" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Filter by currency
curl -X GET "http://localhost:8000/api/v1/accounts/?currency=USD" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Filter by active status
curl -X GET "http://localhost:8000/api/v1/accounts/?is_active=true" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Search accounts
curl -X GET "http://localhost:8000/api/v1/accounts/?search=checking" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Filter by user ID
curl -X GET "http://localhost:8000/api/v1/accounts/?user_id=1" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Get specific account (replace 1 with actual ID)
curl -X GET "http://localhost:8000/api/v1/accounts/1/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Get account summary
curl -X GET "http://localhost:8000/api/v1/accounts/1/summary/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Get accounts statistics
curl -X GET "http://localhost:8000/api/v1/accounts/statistics/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

#### User Profiles Endpoints
```bash
# List all user profiles
curl -X GET "http://localhost:8000/api/v1/user-profiles/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# List with pagination
curl -X GET "http://localhost:8000/api/v1/user-profiles/?page=1&page_size=5" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Filter by user ID
curl -X GET "http://localhost:8000/api/v1/user-profiles/?user_id=1" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Search profiles
curl -X GET "http://localhost:8000/api/v1/user-profiles/?search=john" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Get specific profile
curl -X GET "http://localhost:8000/api/v1/user-profiles/1/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

#### Budgets Endpoints
```bash
# List all budgets
curl -X GET "http://localhost:8000/api/v1/budgets/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# List with pagination
curl -X GET "http://localhost:8000/api/v1/budgets/?page=1&page_size=5" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Filter by period
curl -X GET "http://localhost:8000/api/v1/budgets/?period=MONTHLY" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Filter by active status
curl -X GET "http://localhost:8000/api/v1/budgets/?is_active=true" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Search budgets
curl -X GET "http://localhost:8000/api/v1/budgets/?search=groceries" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Filter by user ID
curl -X GET "http://localhost:8000/api/v1/budgets/?user_id=1" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Get specific budget
curl -X GET "http://localhost:8000/api/v1/budgets/1/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

### 4. Advanced Examples

#### Pretty Print JSON
```bash
# Pretty print the response
curl -X GET "http://localhost:8000/api/v1/accounts/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -s | python -m json.tool
```

#### Save Response to File
```bash
# Save response to file
curl -X GET "http://localhost:8000/api/v1/accounts/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -o accounts_response.json
```

#### Multiple Filters
```bash
# Combine multiple filters
curl -X GET "http://localhost:8000/api/v1/accounts/?account_type=CHECKING&currency=USD&is_active=true&page=1&page_size=5" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

#### Test Error Cases
```bash
# Test non-existent account
curl -X GET "http://localhost:8000/api/v1/accounts/99999/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Test invalid parameters
curl -X GET "http://localhost:8000/api/v1/accounts/?page=0" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"
```

### 5. Quick Test Script

Create a file called `quick_test.sh`:

```bash
#!/bin/bash
SESSION_ID="YOUR_SESSION_ID_HERE"

echo "Testing Accounts API..."

# Test accounts
curl -X GET "http://localhost:8000/api/v1/accounts/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=$SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Test statistics
curl -X GET "http://localhost:8000/api/v1/accounts/statistics/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=$SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"
```

Make it executable and run:
```bash
chmod +x quick_test.sh
./quick_test.sh
```

## Expected Responses

- **200 OK**: Successful request with JSON data
- **401 Unauthorized**: Not authenticated (missing or invalid session cookie)
- **404 Not Found**: Resource not found (invalid ID)
- **400 Bad Request**: Invalid parameters

## Tips

1. **Get your session ID**: Login to Django admin and check browser cookies
2. **Use jq for better formatting**: `curl ... | jq` (if jq is installed)
3. **Check interactive docs**: http://localhost:8000/api/v1/docs
4. **Test with sample data**: Make sure you have data in your database
