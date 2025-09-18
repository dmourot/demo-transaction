#!/bin/bash

# Authenticated CURL Examples for Accounts API
# This script shows how to authenticate and test the API

echo "=== Authenticated CURL Examples for Accounts API ==="
echo ""

# Configuration
BASE_URL="http://localhost:8000"
API_BASE="$BASE_URL/api/v1"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
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
echo -e "${YELLOW}Step 3: Testing API Endpoints${NC}"
echo ""

# Test API endpoints
echo "1. Testing accounts list..."
curl -X GET "$API_BASE/accounts/" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "2. Testing accounts with pagination..."
curl -X GET "$API_BASE/accounts/?page=1&page_size=3" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "3. Testing accounts statistics..."
curl -X GET "$API_BASE/accounts/statistics/" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n"

echo ""
echo "4. Testing user profiles..."
curl -X GET "$API_BASE/user-profiles/" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo "5. Testing budgets..."
curl -X GET "$API_BASE/budgets/" \
  -H "Accept: application/json" \
  -b cookies.txt \
  -w "\nHTTP Status: %{http_code}\n" | head -20

echo ""
echo -e "${GREEN}=== Testing Complete ===${NC}"
echo "You can now use the session cookie for manual testing:"
echo ""
echo "Session cookie file: cookies.txt"
echo "Use it like this:"
echo "curl -X GET \"$API_BASE/accounts/\" -H \"Accept: application/json\" -b cookies.txt"
echo ""
echo "Or get the session ID from the cookie file:"
SESSION_ID=$(grep sessionid cookies.txt | awk '{print $7}')
echo "Session ID: $SESSION_ID"
echo ""
echo "Use it like this:"
echo "curl -X GET \"$API_BASE/accounts/\" -H \"Accept: application/json\" -H \"Cookie: sessionid=$SESSION_ID\""

# Clean up
rm -f cookies.txt
