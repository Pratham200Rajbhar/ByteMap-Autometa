import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def update_testimonial(
    testimonial_id: str,
    author: str = None,
    role: str = None,
    company: str = None,
    content: str = None,
    avatar_url: str = None,
    rating: int = None,
    featured: bool = None
):
    payload = {}
    
    if author is not None:
        payload["author"] = author
    if role is not None:
        payload["role"] = role
    if company is not None:
        payload["company"] = company
    if content is not None:
        payload["content"] = content
    if avatar_url is not None:
        payload["avatar_url"] = avatar_url
    if rating is not None:
        payload["rating"] = rating
    if featured is not None:
        payload["featured"] = featured
    
    response = requests.put(
        f"{API_URL}/testimonials/{testimonial_id}",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
