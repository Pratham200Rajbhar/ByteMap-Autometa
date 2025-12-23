import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import API_URL


def create_comment(
    blog_post_id: str = "",
    author_name: str = "",
    content: str = ""
):
    payload = {
        "blog_post_id": blog_post_id,
        "author_name": author_name,
        "content": content
    }
    
    response = requests.post(f"{API_URL}/comments", json=payload)
    return response.json()
