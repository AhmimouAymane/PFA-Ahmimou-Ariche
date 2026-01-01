import requests
import json
import time
import sys

BASE_URL = "http://localhost:5000"

def wait_for_server():
    print("Waiting for server to be ready...")
    for _ in range(30):  # Wait up to 5 minutes (30 * 10s)
        try:
            response = requests.get(f"{BASE_URL}/api/health")
            if response.status_code == 200:
                print("Server is ready!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        print(".", end="", flush=True)
        time.sleep(10)
    print("\nServer timed out.")
    return False

def test_chat():
    print("\nTesting Chat API...")
    
    # 1. Login/Register (to get token) - simplified, assuming we can create a test user or just use a mock token if auth disabled?
    # Auth is enabled. We need to create a user and login.
    
    # Register
    email = f"test_{int(time.time())}@example.com"
    password = "password123"
    
    try:
        reg_resp = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": email,
            "password": password,
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "preferred_language": "fr"
        })
        
        if reg_resp.status_code == 201:
            print("User registered.")
        else:
            # Maybe already exists, try login
            pass
            
        # Login
        login_resp = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": email,
            "password": password
        })
        
        if login_resp.status_code != 200:
            print(f"Login failed: {login_resp.text}")
            return False
            
        token = login_resp.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Send Message
        print("Sending message: 'Bonjour'")
        chat_resp = requests.post(f"{BASE_URL}/api/chat/message", json={
            "message": "Bonjour, comment obtenir une carte d'identité ?"
        }, headers=headers)
        
        if chat_resp.status_code == 200:
            result = chat_resp.json()
            print("\nResponse Received:")
            print(f"Answer: {result.get('response')}")
            print(f"Sources: {len(result.get('sources', []))}")
            return True
        else:
            print(f"Chat failed: {chat_resp.text}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if wait_for_server():
        if test_chat():
            print("\nVerification SUCCESS")
            sys.exit(0)
        else:
            print("\nVerification FAILED")
            sys.exit(1)
    else:
        sys.exit(1)
