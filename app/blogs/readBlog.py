import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import API_URL


def read_blogs():
    response = requests.get(f"{API_URL}/blog")
    return response.json()


def read_blog_by_id(blog_id: str = ""):
    response = requests.get(f"{API_URL}/blog/{blog_id}")
    return response.json()


def read_blog_by_slug(slug: str = ""):
    response = requests.get(f"{API_URL}/blog/slug/{slug}")
    return response.json()
