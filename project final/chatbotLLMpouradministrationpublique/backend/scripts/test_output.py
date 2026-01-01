import requests
import time

BASE_URL = "http://localhost:5000"

def test_bot(question):
    print(f"\n--- Testing Question: {question} ---")
    
    # Register/Login
    email = "debug@test.com"
    password = "password123"
    
    # Try login
    login_data = {"email": email, "password": password}
    r = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    
    if r.status_code != 200:
        # Try register
        reg_data = {
            "email": email,
            "password": password,
            "username": "debuguser",
            "first_name": "Debug",
            "last_name": "User"
        }
        r = requests.post(f"{BASE_URL}/api/auth/register", json=reg_data)
        if r.status_code != 201:
            print("Failed to login or register")
            return
        token = r.json().get("access_token")
    else:
        token = r.json().get("access_token")
    
    # Send message
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": question}
    r = requests.post(f"{BASE_URL}/api/chat/message", json=payload, headers=headers)
    
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print("FULL JSON RESPONSE:")
        import json
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"Error Content: {r.text}")

if __name__ == "__main__":
    test_bot("Bonjour")
    test_bot("Comment obtenir une carte d'identité?")
    test_bot("كيف أحصل على جواز سفر؟")
