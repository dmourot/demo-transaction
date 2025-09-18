#!/usr/bin/env python
"""
Simple test script to verify the accounts API endpoints.
Run this after starting the Django development server.

Usage:
    python test_api.py
"""

import requests
import json
from getpass import getpass

# Configuration
BASE_URL = "http://localhost:8000/api/v1"

def test_api_endpoints():
    """Test all API endpoints"""
    
    # Create session for authentication
    session = requests.Session()
    
    # Login to get session cookie
    login_url = "http://localhost:8000/admin/login/"
    login_data = {
        'username': USERNAME,
        'password': PASSWORD,
        'csrfmiddlewaretoken': 'test'  # In real scenario, you'd get this from the login page
    }
    
    print("Testing Accounts API endpoints...")
    print("=" * 50)
    
    # Test endpoints
    endpoints = [
        ("GET", "/accounts/", "List all accounts"),
        ("GET", "/accounts/statistics/", "Get accounts statistics"),
        ("GET", "/user-profiles/", "List all user profiles"),
        ("GET", "/budgets/", "List all budgets"),
    ]
    
    for method, endpoint, description in endpoints:
        try:
            url = f"{BASE_URL}{endpoint}"
            print(f"\n{method} {endpoint}")
            print(f"Description: {description}")
            
            if method == "GET":
                response = session.get(url)
            else:
                response = session.get(url)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'accounts' in data:
                    print(f"Found {len(data['accounts'])} accounts")
                elif isinstance(data, dict) and 'profiles' in data:
                    print(f"Found {len(data['profiles'])} profiles")
                elif isinstance(data, dict) and 'budgets' in data:
                    print(f"Found {len(data['budgets'])} budgets")
                else:
                    print(f"Response: {json.dumps(data, indent=2)[:200]}...")
            else:
                print(f"Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to server. Make sure Django is running on localhost:8000")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 50)
    print("API Documentation available at: http://localhost:8000/api/v1/docs")
    print("Swagger UI available at: http://localhost:8000/api/v1/swagger")

if __name__ == "__main__":
    test_api_endpoints()
