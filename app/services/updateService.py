import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def update_service(
    service_id: str,
    title: str = None,
    description: str = None,
    icon: str = None,
    features: list = None,
    technologies: list = None
):
    payload = {}
    
    if title is not None:
        payload["title"] = title
    if description is not None:
        payload["description"] = description
    if icon is not None:
        payload["icon"] = icon
    if features is not None:
        payload["features"] = features
    if technologies is not None:
        payload["technologies"] = technologies
    
    response = requests.put(
        f"{API_URL}/services/{service_id}",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
