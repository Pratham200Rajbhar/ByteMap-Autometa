import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def create_project(
    title: str = "",
    category: str = "",
    description: str = "",
    long_description: str = "",
    technologies: list = None,
    gradient: str = "",
    metrics: dict = None,
    year: str = "",
    client_name: str = "",
    live_url: str = "",
    github_url: str = ""
):
    payload = {
        "title": title,
        "category": category,
        "description": description,
        "long_description": long_description,
        "technologies": technologies or [],
        "gradient": gradient,
        "metrics": metrics or {},
        "year": year,
        "client_name": client_name,
        "live_url": live_url,
        "github_url": github_url
    }
    
    response = requests.post(
        f"{API_URL}/projects",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    return response.json()
