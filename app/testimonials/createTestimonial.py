import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def create_testimonial(
    author: str = "",
    role: str = "",
    company: str = "",
    content: str = "",
    avatar_url: str = "",
    rating: int = 5,
    featured: bool = False
):
    payload = {
        "author": author,
        "role": role,
        "company": company,
        "content": content,
        "avatar_url": avatar_url,
        "rating": rating,
        "featured": featured
    }
    
    response = requests.post(
        f"{API_URL}/testimonials",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
