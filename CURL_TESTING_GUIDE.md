# CURL Testing Guide for Accounts API

## Prerequisites
1. Start the Django server: `python manage.py runserver`
2. Make sure you have some sample data in your database
3. You need to be authenticated to access the API endpoints

## Quick Test (Without Authentication)
These commands will return 401 Unauthorized, but they test the basic connectivity:

```bash
# Test basic connectivity
curl -X GET "http://localhost:8000/api/v1/accounts/" -w "\nHTTP Status: %{http_code}\n"

# Test with JSON accept header
curl -X GET "http://localhost:8000/api/v1/accounts/" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n"

# Test pagination parameters
curl -X GET "http://localhost:8000/api/v1/accounts/?page=1&page_size=5" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n"
```

## Authentication Methods

### Method 1: Session Cookie Authentication

1. **Login via browser:**
   - Go to http://localhost:8000/admin/
   - Login with your Django superuser credentials
   - Open browser dev tools (F12) → Network tab
   - Look for any request to see the session cookie

2. **Use the session cookie in curl:**
```bash
# Replace YOUR_SESSION_ID with actual session ID from browser
curl -X GET "http://localhost:8000/api/v1/accounts/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"
```

### Method 2: Programmatic Authentication

Create a script to get the session cookie:

```bash
# Get CSRF token and session cookie
CSRF_TOKEN=$(curl -s -c cookies.txt "http://localhost:8000/admin/login/" | grep csrftoken | sed 's/.*value="\([^"]*\)".*/\1/')

# Login and get session
curl -s -b cookies.txt -c cookies.txt -X POST "http://localhost:8000/admin/login/" \
  -H "Referer: http://localhost:8000/admin/login/" \
  -H "X-CSRFToken: $CSRF_TOKEN" \
  -d "username=YOUR_USERNAME&password=YOUR_PASSWORD&csrfmiddlewaretoken=$CSRF_TOKEN"

# Now use the session cookie
curl -X GET "http://localhost:8000/api/v1/accounts/" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n"
```

## Complete API Testing Commands

### 1. Accounts Endpoints

```bash
# List all accounts
curl -X GET "http://localhost:8000/api/v1/accounts/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# List accounts with pagination
curl -X GET "http://localhost:8000/api/v1/accounts/?page=1&page_size=10" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Filter by account type
curl -X GET "http://localhost:8000/api/v1/accounts/?account_type=CHECKING" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Filter by currency
curl -X GET "http://localhost:8000/api/v1/accounts/?currency=USD" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Filter by active status
curl -X GET "http://localhost:8000/api/v1/accounts/?is_active=true" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Search accounts
curl -X GET "http://localhost:8000/api/v1/accounts/?search=checking" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Filter by user ID
curl -X GET "http://localhost:8000/api/v1/accounts/?user_id=1" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Get specific account (replace 1 with actual ID)
curl -X GET "http://localhost:8000/api/v1/accounts/1/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Get account summary
curl -X GET "http://localhost:8000/api/v1/accounts/1/summary/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Get accounts statistics
curl -X GET "http://localhost:8000/api/v1/accounts/statistics/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"
```

### 2. User Profiles Endpoints

```bash
# List all user profiles
curl -X GET "http://localhost:8000/api/v1/user-profiles/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# List profiles with pagination
curl -X GET "http://localhost:8000/api/v1/user-profiles/?page=1&page_size=5" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Filter by user ID
curl -X GET "http://localhost:8000/api/v1/user-profiles/?user_id=1" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Search profiles
curl -X GET "http://localhost:8000/api/v1/user-profiles/?search=john" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Get specific profile
curl -X GET "http://localhost:8000/api/v1/user-profiles/1/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"
```

### 3. Budgets Endpoints

```bash
# List all budgets
curl -X GET "http://localhost:8000/api/v1/budgets/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# List budgets with pagination
curl -X GET "http://localhost:8000/api/v1/budgets/?page=1&page_size=5" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Filter by period
curl -X GET "http://localhost:8000/api/v1/budgets/?period=MONTHLY" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Filter by active status
curl -X GET "http://localhost:8000/api/v1/budgets/?is_active=true" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Search budgets
curl -X GET "http://localhost:8000/api/v1/budgets/?search=groceries" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Filter by user ID
curl -X GET "http://localhost:8000/api/v1/budgets/?user_id=1" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"

# Get specific budget
curl -X GET "http://localhost:8000/api/v1/budgets/1/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"
```

## Advanced Testing

### Combined Filters
```bash
# Multiple filters
curl -X GET "http://localhost:8000/api/v1/accounts/?account_type=CHECKING&currency=USD&is_active=true&page=1&page_size=5" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -w "\nHTTP Status: %{http_code}\n"
```

### Pretty Print JSON
```bash
# Pretty print the JSON response
curl -X GET "http://localhost:8000/api/v1/accounts/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -s | python -m json.tool
```

### Save Response to File
```bash
# Save response to file
curl -X GET "http://localhost:8000/api/v1/accounts/" \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -o accounts_response.json
```

## Error Testing

### Test Invalid Endpoints
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

## Running the Test Script

Make the script executable and run it:
```bash
chmod +x curl_test_commands.sh
./curl_test_commands.sh
```

## Expected Responses

- **200 OK**: Successful request with data
- **401 Unauthorized**: Not authenticated
- **404 Not Found**: Resource not found
- **400 Bad Request**: Invalid parameters

## Tips

1. **Get your session ID**: Login to Django admin and check browser cookies
2. **Use jq for better JSON formatting**: `curl ... | jq`
3. **Test with different data**: Make sure you have sample data in your database
4. **Check the interactive docs**: http://localhost:8000/api/v1/docs for testing
