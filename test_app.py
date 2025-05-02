import requests
import sys
import uuid

# Base URL
BASE_URL = 'http://localhost:8000'

def test_create_user():
    """Test user creation with API call"""
    print("Testing user creation...")
    
    # Create a unique username for testing
    unique_id = uuid.uuid4().hex[:8]
    
    # Create a user
    user_data = {
        'user_name': f'testuser_{unique_id}',
        'email': f'{unique_id}@example.com',
        'password': 'testpassword123',
        'is_admin': '0'
    }
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(f'{BASE_URL}/app/createUser', data=user_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        # Store the created user credentials for login
        global created_username, created_password
        created_username = user_data['user_name']
        created_password = user_data['password']
        return True
    
    return False

def test_login():
    """Test login with API call"""
    print("\nTesting login...")
    
    # Start a session to maintain cookies
    session = requests.Session()
    
    # Login
    login_data = {
        'username': created_username,
        'password': created_password
    }
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = session.post(f'{BASE_URL}/login/', data=login_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # If login successful, check if we can access the index page as logged in user
    if response.status_code == 200:
        print("\nAccessing index page as logged in user...")
        response = session.get(f'{BASE_URL}/')
        print(f"Status Code: {response.status_code}")
        
        # Check if username is in the response
        if created_username in response.text:
            print("User is logged in correctly!")
            return True
        else:
            print("User seems to be not logged in.")
            return False
    
    return False

def main():
    # Run tests
    user_created = test_create_user()
    if not user_created:
        print("User creation failed. Exiting.")
        sys.exit(1)
    
    login_successful = test_login()
    if not login_successful:
        print("Login failed. Exiting.")
        sys.exit(1)
    
    print("\nAll tests passed successfully!")

if __name__ == "__main__":
    main() 