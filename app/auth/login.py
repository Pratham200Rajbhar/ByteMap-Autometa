import requests
from config import API_URL
import os

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# print(f"DEBUG: Attempting login for {USERNAME}")
response = requests.post(API_URL + "/auth/login", json={"username": USERNAME, "pin": PASSWORD})
if response.status_code != 200:
    print(f"ERROR: Login failed with status {response.status_code}")
    print(f"RESPONSE: {response.text}")
    auth_token = None
else:
    try:
        auth_token = response.json()["token"]
    except KeyError:
        print(f"ERROR: 'token' not found in response: {response.json()}")
        auth_token = None

