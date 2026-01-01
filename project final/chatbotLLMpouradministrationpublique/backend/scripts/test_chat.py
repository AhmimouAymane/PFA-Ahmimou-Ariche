import requests
import time

# Register
email = f'test{int(time.time())}@example.com'
username = f'user{int(time.time())}'

print("=== TESTING CHATBOT ===\n")

# Step 1: Register
print("1. Registering user...")
r = requests.post('http://localhost:5000/api/auth/register', json={
    'email': email,
    'password': 'password123',
    'username': username,
    'first_name': 'Test',
    'last_name': 'User',
    'preferred_language': 'fr'
})
print(f"   Status: {r.status_code}")
if r.status_code == 201:
    token = r.json()['access_token']
    print(f"   ✓ User registered successfully")
else:
    print(f"   ✗ Registration failed: {r.text}")
    exit(1)

# Step 2: Send chat message
print("\n2. Sending chat message...")
print("   Question: 'Comment obtenir une carte d'identité?'")
r2 = requests.post('http://localhost:5000/api/chat/message', 
    json={'message': "Comment obtenir une carte d'identité?"},
    headers={'Authorization': f'Bearer {token}'}
)
print(f"   Status: {r2.status_code}")
if r2.status_code == 200:
    result = r2.json()
    print(f"   ✓ Chat response received")
    print(f"\n   RESPONSE:")
    print(f"   {result.get('response', 'No response')}")
    print(f"\n   Sources: {len(result.get('sources', []))}")
    print(f"   Language: {result.get('language', 'unknown')}")
else:
    print(f"   ✗ Chat failed: {r2.text}")
    exit(1)

print("\n=== ALL TESTS PASSED ===")
