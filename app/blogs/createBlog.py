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
    category: str = "",
    author_name: str = "",
    author_initials: str = "",
    author_role: str = "",
    read_time: str = "",
    gradient: str = "",
    featured: bool = False,
    published: bool = False
):
    payload = {
        "title": title,
        "excerpt": excerpt,
        "content": content,
        "category": category,
        "author_name": author_name,
        "author_initials": author_initials,
        "author_role": author_role,
        "read_time": read_time,
        "gradient": gradient,
        "featured": featured,
        "published": published
    }
    
    response = requests.post(
        f"{API_URL}/blog",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
