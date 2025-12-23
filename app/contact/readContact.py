import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def read_contacts():
    response = requests.get(
        f"{API_URL}/contact",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    return response.json()
