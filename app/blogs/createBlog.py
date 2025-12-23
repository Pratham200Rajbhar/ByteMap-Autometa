import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def create_blog(
    title: str = "",
    excerpt: str = "",
    content: str = "",
    category: str = ""
):
    payload = {
        "title": title,
        "excerpt": excerpt,
        "content": content,
        "category": category,
        "author_name": "Pratham",
        "author_initials": "P",
        "author_role": "CEO & Founder",
        "read_time": "5 min read",
        "gradient": "bg-gradient-to-r from-blue-500 to-indigo-500",
        "featured": True,
        "published": True
    }
    
    response = requests.post(
        f"{API_URL}/blog",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
