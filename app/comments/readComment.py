import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def read_comments():
    response = requests.get(
        f"{API_URL}/comments",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    return response.json()


def read_comments_by_post(blog_post_id: str = ""):
    response = requests.get(f"{API_URL}/comments/post/{blog_post_id}")
    return response.json()
