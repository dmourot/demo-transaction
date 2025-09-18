#!/bin/bash

# Authenticated CURL Examples for Transaction API
# This script shows how to authenticate and test the transaction API

echo "=== Authenticated CURL Examples for Transaction API ==="
echo ""

# Configuration
BASE_URL="http://localhost:8000"
API_BASE="$BASE_URL/api/v1"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${YELLOW}Step 1: Get CSRF Token and Session Cookie${NC}"
echo ""

# Get CSRF token and initial session
echo "Getting CSRF token..."
CSRF_TOKEN=$(curl -s -c cookies.txt "$BASE_URL/admin/login/" | grep csrftoken | sed 's/.*value="\([^"]*\)".*/\1/')

if [ -z "$CSRF_TOKEN" ]; then
    echo -e "${RED}Failed to get CSRF token. Make sure Django server is running.${NC}"
    exit 1
fi

echo "CSRF Token: $CSRF_TOKEN"
echo ""

# Login (replace with your actual credentials)
echo -e "${YELLOW}Step 2: Login (you'll need to enter your Django admin credentials)${NC}"
echo "Enter your Django admin username:"
read -r USERNAME
echo "Enter your Django admin password:"
read -s PASSWORD

echo ""
echo "Logging in..."

# Login and get session cookie
LOGIN_RESPONSE=$(curl -s -b cookies.txt -c cookies.txt -X POST "$BASE_URL/admin/login/" \
  -H "Referer: $BASE_URL/admin/login/" \
  -H "X-CSRFToken: $CSRF_TOKEN" \
  -d "username=$USERNAME&password=$PASSWORD&csrfmiddlewaretoken=$CSRF_TOKEN" \
  -w "HTTP_STATUS:%{http_code}")

HTTP_STATUS=$(echo "$LOGIN_RESPONSE" | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)

if [ "$HTTP_STATUS" = "200" ]; then
    echo -e "${GREEN}Login successful!${NC}"
else
    echo -e "${RED}Login failed. Please check your credentials.${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 3: Testing Transaction API Endpoints${NC}"
echo ""

# Test Categories API
echo -e "${BLUE}=== Testing Categories API ===${NC}"
echo ""

echo "1. Testing categories list..."
curl -X GET "$API_BASE/categories/" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "2. Testing categories with pagination..."
curl -X GET "$API_BASE/categories/?page=1&page_size=3" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "3. Testing categories by type..."
curl -X GET "$API_BASE/categories/?category_type=INCOME" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "4. Testing root categories..."
curl -X GET "$API_BASE/categories/?parent_id=0" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "5. Testing specific category..."
curl -X GET "$API_BASE/categories/1/" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n"

# Test Transactions API
echo ""
echo -e "${BLUE}=== Testing Transactions API ===${NC}"
echo ""

echo "6. Testing transactions list..."
curl -X GET "$API_BASE/transactions/" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "7. Testing transactions with pagination..."
curl -X GET "$API_BASE/transactions/?page=1&page_size=3" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "8. Testing transactions by type..."
curl -X GET "$API_BASE/transactions/?transaction_type=INCOME" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "9. Testing transactions by account..."
curl -X GET "$API_BASE/transactions/?account_id=1" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "10. Testing transactions by date range..."
curl -X GET "$API_BASE/transactions/?date_from=2024-01-01&date_to=2024-12-31" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "11. Testing transactions by amount range..."
curl -X GET "$API_BASE/transactions/?min_amount=10.00&max_amount=100.00" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "12. Testing transactions search..."
curl -X GET "$API_BASE/transactions/?search=groceries" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "13. Testing specific transaction..."
curl -X GET "$API_BASE/transactions/1/" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n"

echo ""
echo "14. Testing transaction summary..."
curl -X GET "$API_BASE/transactions/1/summary/" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n"

echo ""
echo "15. Testing transactions statistics..."
curl -X GET "$API_BASE/transactions/statistics/" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n"

# Test Recurring Transactions API
echo ""
echo -e "${BLUE}=== Testing Recurring Transactions API ===${NC}"
echo ""

echo "16. Testing recurring transactions list..."
curl -X GET "$API_BASE/recurring-transactions/" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "17. Testing recurring transactions with pagination..."
curl -X GET "$API_BASE/recurring-transactions/?page=1&page_size=3" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "18. Testing recurring transactions by user..."
curl -X GET "$API_BASE/recurring-transactions/?user_id=1" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "19. Testing recurring transactions by frequency..."
curl -X GET "$API_BASE/recurring-transactions/?frequency=MONTHLY" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "20. Testing specific recurring transaction..."
curl -X GET "$API_BASE/recurring-transactions/1/" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n"

# Test Complex Filtering
echo ""
echo -e "${BLUE}=== Testing Complex Filtering ===${NC}"
echo ""

echo "21. Testing complex transaction filter..."
curl -X GET "$API_BASE/transactions/?transaction_type=EXPENSE&account_id=1&date_from=2024-01-01&min_amount=50.00&is_verified=true" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "22. Testing category hierarchy..."
curl -X GET "$API_BASE/categories/?parent_id=1" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "23. Testing payment method distribution..."
curl -X GET "$API_BASE/transactions/?payment_method=CASH" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "24. Testing recurring vs non-recurring transactions..."
curl -X GET "$API_BASE/transactions/?is_recurring=true" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "25. Testing verified vs unverified transactions..."
curl -X GET "$API_BASE/transactions/?is_verified=false" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo -e "${GREEN}=== Testing Complete ===${NC}"
echo "All transaction API endpoints have been tested with authentication!"
echo ""

echo "You can now use the session cookie for manual testing:"
echo ""
echo "Session cookie file: cookies.txt"
echo "Use it like this:"
echo "curl -X GET \"$API_BASE/transactions/\" -H \"Accept: application/json\" -b cookies.txt"
echo ""

echo "Or get the session ID from the cookie file:"
SESSION_ID=$(grep sessionid cookies.txt | awk '{print $7}')
echo "Session ID: $SESSION_ID"
echo ""
echo "Use it like this:"
echo "curl -X GET \"$API_BASE/transactions/\" -H \"Accept: application/json\" -H \"Cookie: sessionid=$SESSION_ID\""

# Clean up
rm -f cookies.txt
