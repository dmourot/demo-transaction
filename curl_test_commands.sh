#!/bin/bash

# API Testing Script with curl commands
# Make sure to start the Django server first: python manage.py runserver

echo "=== Accounts API Testing with curl ==="
echo "Make sure Django server is running on localhost:8000"
echo "You need to be authenticated to use these endpoints"
echo ""

# Base URL
BASE_URL="http://localhost:8000/api/v1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}1. Testing without authentication (should return 401)${NC}"
echo "curl -X GET \"$BASE_URL/accounts/\""
curl -X GET "$BASE_URL/accounts/" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}2. Get accounts with basic curl (will fail without auth)${NC}"
echo "curl -X GET \"$BASE_URL/accounts/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/accounts/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}3. Get accounts with pagination parameters${NC}"
echo "curl -X GET \"$BASE_URL/accounts/?page=1&page_size=5\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/accounts/?page=1&page_size=5" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}4. Filter accounts by type${NC}"
echo "curl -X GET \"$BASE_URL/accounts/?account_type=CHECKING\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/accounts/?account_type=CHECKING" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}5. Search accounts${NC}"
echo "curl -X GET \"$BASE_URL/accounts/?search=checking\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/accounts/?search=checking" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}6. Get specific account (replace 1 with actual account ID)${NC}"
echo "curl -X GET \"$BASE_URL/accounts/1/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/accounts/1/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}7. Get account summary${NC}"
echo "curl -X GET \"$BASE_URL/accounts/1/summary/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/accounts/1/summary/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}8. Get accounts statistics${NC}"
echo "curl -X GET \"$BASE_URL/accounts/statistics/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/accounts/statistics/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}9. Get user profiles${NC}"
echo "curl -X GET \"$BASE_URL/user-profiles/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/user-profiles/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}10. Get specific user profile${NC}"
echo "curl -X GET \"$BASE_URL/user-profiles/1/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/user-profiles/1/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}11. Get budgets${NC}"
echo "curl -X GET \"$BASE_URL/budgets/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/budgets/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}12. Filter budgets by period${NC}"
echo "curl -X GET \"$BASE_URL/budgets/?period=MONTHLY\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/budgets/?period=MONTHLY" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}13. Get specific budget${NC}"
echo "curl -X GET \"$BASE_URL/budgets/1/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/budgets/1/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${GREEN}=== AUTHENTICATED REQUESTS ===${NC}"
echo "To test with authentication, you need to:"
echo "1. Login to Django admin: http://localhost:8000/admin/"
echo "2. Get your session cookie"
echo "3. Use the cookie in curl requests"
echo ""

echo -e "${YELLOW}Example with session cookie:${NC}"
echo "curl -X GET \"$BASE_URL/accounts/\" \\"
echo "  -H \"Accept: application/json\" \\"
echo "  -H \"Cookie: sessionid=YOUR_SESSION_ID\""
echo ""

echo -e "${YELLOW}Example with CSRF token:${NC}"
echo "curl -X GET \"$BASE_URL/accounts/\" \\"
echo "  -H \"Accept: application/json\" \\"
echo "  -H \"Cookie: sessionid=YOUR_SESSION_ID; csrftoken=YOUR_CSRF_TOKEN\" \\"
echo "  -H \"X-CSRFToken: YOUR_CSRF_TOKEN\""
echo ""

echo -e "${GREEN}=== API DOCUMENTATION ===${NC}"
echo "Interactive documentation: http://localhost:8000/api/v1/docs"
echo "Swagger UI: http://localhost:8000/api/v1/swagger"
echo "ReDoc: http://localhost:8000/api/v1/redoc"
