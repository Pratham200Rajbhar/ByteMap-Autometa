import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def update_project(
    slug: str,
    title: str = None,
    category: str = None,
    description: str = None,
    long_description: str = None,
    technologies: list = None,
    gradient: str = None,
    metrics: dict = None,
    year: str = None,
    client_name: str = None,
    live_url: str = None,
    github_url: str = None,
    featured: bool = None
):
    payload = {}
    
    if title is not None:
        payload["title"] = title
    if category is not None:
        payload["category"] = category
    if description is not None:
        payload["description"] = description
    if long_description is not None:
        payload["long_description"] = long_description
    if technologies is not None:
        payload["technologies"] = technologies
    if gradient is not None:
        payload["gradient"] = gradient
    if metrics is not None:
        payload["metrics"] = metrics
    if year is not None:
        payload["year"] = year
    if client_name is not None:
        payload["client_name"] = client_name
    if live_url is not None:
        payload["live_url"] = live_url
    if github_url is not None:
        payload["github_url"] = github_url
    if featured is not None:
        payload["featured"] = featured
    
    response = requests.put(
        f"{API_URL}/projects/{slug}",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
