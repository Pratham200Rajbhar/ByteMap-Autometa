import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL

response = requests.post(API_URL + "/blog", json={
    "title": "Test Blog",
    "excerpt": "This is a test blog",
    "content": "This is a test blog",
    "category": "Test Category",
    "author_name": "Test Author",
    "author_initials": "TA",
    "author_role": "Test Role",
    "read_time": "10 min",
    "gradient": "from-blue-600 to-cyan-600",
    "featured": True,
    "published": True
}, headers={"Authorization": f"Bearer {auth_token}"})

print(response.json())
