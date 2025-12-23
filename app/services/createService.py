import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def create_service(
    title: str = "",
    description: str = "",
    icon: str = "",
    features: list = None,
    technologies: list = None
):
    payload = {
        "title": title,
        "description": description,
        "icon": icon,
        "features": features or [],
        "technologies": technologies or []
    }
    
    response = requests.post(
        f"{API_URL}/services",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    return response.json()
