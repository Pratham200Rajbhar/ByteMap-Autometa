import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL

testimonial_data = {
    "name": "Jane Doe",
    "role": "CEO at TechInnovate",
    "content": "ByteMap delivered an exceptional product that exceeded our expectations.",
    "avatar_url": "https://example.com/avatar.jpg",
    "featured": True
}

response = requests.post(
    f"{API_URL}/testimonials", 
    json=testimonial_data, 
    headers={"Authorization": f"Bearer {auth_token}"}
)

print(response.json())
