import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def update_blog(
    slug: str,
    title: str = None,
    excerpt: str = None,
    content: str = None,
    category: str = None,
    author_name: str = None,
    author_initials: str = None,
    author_role: str = None,
    read_time: str = None,
    gradient: str = None,
    featured: bool = None,
    published: bool = None
):
    payload = {}
    
    if title is not None:
        payload["title"] = title
    if excerpt is not None:
        payload["excerpt"] = excerpt
    if content is not None:
        payload["content"] = content
    if category is not None:
        payload["category"] = category
    if author_name is not None:
        payload["author_name"] = author_name
    if author_initials is not None:
        payload["author_initials"] = author_initials
    if author_role is not None:
        payload["author_role"] = author_role
    if read_time is not None:
        payload["read_time"] = read_time
    if gradient is not None:
        payload["gradient"] = gradient
    if featured is not None:
        payload["featured"] = featured
    if published is not None:
        payload["published"] = published
    
    response = requests.put(
        f"{API_URL}/blog/{slug}",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
