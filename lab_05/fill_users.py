import requests
import random
import string

API_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{API_URL}/token"
CREATE_USER_ENDPOINT = f"{API_URL}/users/"
CACHE_WARMUP_ENDPOINT = f"{API_URL}/users/withcache/"
USERNAMES = []

login_data = {
    "username": "admin",
    "password": "secret"
}

resp = requests.post(LOGIN_ENDPOINT, data=login_data)
if resp.status_code != 200:
    print("Login failed:", resp.text)
    exit(1)

access_token = resp.json().get("access_token")
headers = {"Authorization": f"Bearer {access_token}"}

def random_username(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

for _ in range(100):
    username = random_username()
    USERNAMES.append(username)
    payload = {
        "username": username,
        "email": f"{username}@example.com",
        "full_name": f"{username.capitalize()} User",
        "password": "password123"
    }
    response = requests.post(CREATE_USER_ENDPOINT, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"Created user: {username}")
    else:
        print(f"Failed to create user {username}: {response.text}")


with open("usernames.txt", "w") as f:
    for name in USERNAMES:
        f.write(name + "\n")

with open("usernames.txt", "r") as f:
    usernames = [line.strip() for line in f.readlines() if line.strip()]


print("Warming up cache...")
for username in usernames:
    url = f"{CACHE_WARMUP_ENDPOINT}{username}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to warm up cache for {username}: {response.status_code}")
