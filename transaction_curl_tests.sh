#!/bin/bash

# Transaction API Testing Script with curl commands
# Make sure to start the Django server first: python manage.py runserver

echo "=== Transaction API Testing with curl ==="
echo "Make sure Django server is running on localhost:8000"
echo "You need to be authenticated to use these endpoints"
echo ""

# Base URL
BASE_URL="http://localhost:8000/api/v1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}1. Testing without authentication (should return 401)${NC}"
echo "curl -X GET \"$BASE_URL/transactions/\""
curl -X GET "$BASE_URL/transactions/" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${BLUE}=== CATEGORIES API ===${NC}"
echo ""

echo -e "${YELLOW}2. Get all categories${NC}"
echo "curl -X GET \"$BASE_URL/categories/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/categories/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}3. Get categories with pagination${NC}"
echo "curl -X GET \"$BASE_URL/categories/?page=1&page_size=5\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/categories/?page=1&page_size=5" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}4. Filter categories by type${NC}"
echo "curl -X GET \"$BASE_URL/categories/?category_type=INCOME\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/categories/?category_type=INCOME" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}5. Filter categories by active status${NC}"
echo "curl -X GET \"$BASE_URL/categories/?is_active=true\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/categories/?is_active=true" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}6. Get root categories only${NC}"
echo "curl -X GET \"$BASE_URL/categories/?parent_id=0\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/categories/?parent_id=0" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}7. Search categories${NC}"
echo "curl -X GET \"$BASE_URL/categories/?search=food\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/categories/?search=food" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}8. Get specific category (replace 1 with actual category ID)${NC}"
echo "curl -X GET \"$BASE_URL/categories/1/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/categories/1/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${BLUE}=== TRANSACTIONS API ===${NC}"
echo ""

echo -e "${YELLOW}9. Get all transactions${NC}"
echo "curl -X GET \"$BASE_URL/transactions/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}10. Get transactions with pagination${NC}"
echo "curl -X GET \"$BASE_URL/transactions/?page=1&page_size=5\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/?page=1&page_size=5" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}11. Filter transactions by type${NC}"
echo "curl -X GET \"$BASE_URL/transactions/?transaction_type=INCOME\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/?transaction_type=INCOME" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}12. Filter transactions by account${NC}"
echo "curl -X GET \"$BASE_URL/transactions/?account_id=1\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/?account_id=1" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}13. Filter transactions by category${NC}"
echo "curl -X GET \"$BASE_URL/transactions/?category_id=1\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/?category_id=1" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}14. Filter transactions by payment method${NC}"
echo "curl -X GET \"$BASE_URL/transactions/?payment_method=CASH\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/?payment_method=CASH" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}15. Filter transactions by recurring status${NC}"
echo "curl -X GET \"$BASE_URL/transactions/?is_recurring=true\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/?is_recurring=true" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}16. Filter transactions by verification status${NC}"
echo "curl -X GET \"$BASE_URL/transactions/?is_verified=true\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/?is_verified=true" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}17. Filter transactions by date range${NC}"
echo "curl -X GET \"$BASE_URL/transactions/?date_from=2024-01-01&date_to=2024-12-31\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/?date_from=2024-01-01&date_to=2024-12-31" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}18. Filter transactions by amount range${NC}"
echo "curl -X GET \"$BASE_URL/transactions/?min_amount=10.00&max_amount=100.00\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/?min_amount=10.00&max_amount=100.00" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}19. Search transactions${NC}"
echo "curl -X GET \"$BASE_URL/transactions/?search=groceries\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/?search=groceries" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}20. Filter transactions by user${NC}"
echo "curl -X GET \"$BASE_URL/transactions/?user_id=1\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/?user_id=1" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}21. Get specific transaction (replace 1 with actual transaction ID)${NC}"
echo "curl -X GET \"$BASE_URL/transactions/1/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/1/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}22. Get transaction summary${NC}"
echo "curl -X GET \"$BASE_URL/transactions/1/summary/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/1/summary/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}23. Get transactions statistics${NC}"
echo "curl -X GET \"$BASE_URL/transactions/statistics/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/statistics/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${BLUE}=== RECURRING TRANSACTIONS API ===${NC}"
echo ""

echo -e "${YELLOW}24. Get all recurring transactions${NC}"
echo "curl -X GET \"$BASE_URL/recurring-transactions/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/recurring-transactions/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}25. Get recurring transactions with pagination${NC}"
echo "curl -X GET \"$BASE_URL/recurring-transactions/?page=1&page_size=5\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/recurring-transactions/?page=1&page_size=5" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}26. Filter recurring transactions by user${NC}"
echo "curl -X GET \"$BASE_URL/recurring-transactions/?user_id=1\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/recurring-transactions/?user_id=1" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}27. Filter recurring transactions by account${NC}"
echo "curl -X GET \"$BASE_URL/recurring-transactions/?account_id=1\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/recurring-transactions/?account_id=1" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}28. Filter recurring transactions by type${NC}"
echo "curl -X GET \"$BASE_URL/recurring-transactions/?transaction_type=EXPENSE\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/recurring-transactions/?transaction_type=EXPENSE" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}29. Filter recurring transactions by frequency${NC}"
echo "curl -X GET \"$BASE_URL/recurring-transactions/?frequency=MONTHLY\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/recurring-transactions/?frequency=MONTHLY" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}30. Filter recurring transactions by active status${NC}"
echo "curl -X GET \"$BASE_URL/recurring-transactions/?is_active=true\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/recurring-transactions/?is_active=true" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}31. Search recurring transactions${NC}"
echo "curl -X GET \"$BASE_URL/recurring-transactions/?search=rent\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/recurring-transactions/?search=rent" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}32. Get specific recurring transaction (replace 1 with actual ID)${NC}"
echo "curl -X GET \"$BASE_URL/recurring-transactions/1/\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/recurring-transactions/1/" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${GREEN}=== AUTHENTICATED REQUESTS ===${NC}"
echo "To test with authentication, you need to:"
echo "1. Login to Django admin: http://localhost:8000/admin/"
echo "2. Get your session cookie"
echo "3. Use the cookie in curl requests"
echo ""

echo -e "${YELLOW}Example with session cookie:${NC}"
echo "curl -X GET \"$BASE_URL/transactions/\" \\"
echo "  -H \"Accept: application/json\" \\"
echo "  -H \"Cookie: sessionid=YOUR_SESSION_ID\""
echo ""

echo -e "${YELLOW}Example with CSRF token:${NC}"
echo "curl -X GET \"$BASE_URL/transactions/\" \\"
echo "  -H \"Accept: application/json\" \\"
echo "  -H \"Cookie: sessionid=YOUR_SESSION_ID; csrftoken=YOUR_CSRF_TOKEN\" \\"
echo "  -H \"X-CSRFToken: YOUR_CSRF_TOKEN\""
echo ""

echo -e "${GREEN}=== COMBINED FILTERING EXAMPLES ===${NC}"
echo ""

echo -e "${YELLOW}Complex transaction filter example:${NC}"
echo "curl -X GET \"$BASE_URL/transactions/?transaction_type=EXPENSE&account_id=1&date_from=2024-01-01&min_amount=50.00&is_verified=true\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/transactions/?transaction_type=EXPENSE&account_id=1&date_from=2024-01-01&min_amount=50.00&is_verified=true" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${YELLOW}Category filter with parent/child relationship:${NC}"
echo "curl -X GET \"$BASE_URL/categories/?parent_id=1\" -H \"Accept: application/json\""
curl -X GET "$BASE_URL/categories/?parent_id=1" -H "Accept: application/json" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo -e "${GREEN}=== API DOCUMENTATION ===${NC}"
echo "Interactive documentation: http://localhost:8000/api/v1/docs"
echo "Swagger UI: http://localhost:8000/api/v1/swagger"
echo "ReDoc: http://localhost:8000/api/v1/redoc"
echo ""

echo -e "${GREEN}=== TESTING COMPLETE ===${NC}"
echo "All transaction API endpoints have been tested!"
echo "Check the HTTP status codes to verify authentication requirements."
