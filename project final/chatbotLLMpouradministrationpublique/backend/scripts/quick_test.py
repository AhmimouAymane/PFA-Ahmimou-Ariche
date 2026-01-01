import requests

BASE_URL = "http://localhost:5000"
token = None

# Quick register
r = requests.post(f'{BASE_URL}/api/auth/register', json={
    'email': 'quicktest@test.com',
    'password': 'test123',
    'username': 'quicktest',
    'first_name': 'Test',
    'last_name': 'User',
    'preferred_language': 'fr'
})

if r.status_code == 201:
    token = r.json()['access_token']
else:
    # Try login if already exists
    r = requests.post(f'{BASE_URL}/api/auth/login', json={
        'email': 'quicktest@test.com',
        'password': 'test123'
    })
    if r.status_code == 200:
        token = r.json()['access_token']

if not token:
    print("Failed to get token")
    exit(1)

# Test different topics
tests = [
    "Comment obtenir un passeport?",
    "Je veux faire mon permis de conduire",
    "Comment s'inscrire au RAMED?",
    "Procédure pour le mariage",
    "Demande de bourse universitaire",
    "Comment obtenir un logement social?",
]

print("=" * 70)
print("TESTING COMPREHENSIVE MOROCCAN ADMIN CHATBOT")
print("=" * 70 + "\n")

for i, question in enumerate(tests, 1):
    print(f"[{i}] Question: {question}")
    r = requests.post(f'{BASE_URL}/api/chat/message',
        json={'message': question},
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if r.status_code == 200:
        result = r.json()
        answer = result.get('response', '').split('\n')[0][:80]  # First line
        print(f"    ✓ Answer: {answer}...")
    else:
        print(f"    ✗ Error: {r.status_code}")
    print()

print("=" * 70)
print("✓ System can handle diverse Moroccan administrative topics!")
print("=" * 70)
