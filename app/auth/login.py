import requests
from config import API_URL

auth_token = requests.post(API_URL + "/auth/login", json={"username": "apple", "pin": "147258"})
auth_token = auth_token.json()["token"]

