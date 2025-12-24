import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def create_milestone(
    year: str = "",
    title: str = "",
    description: str = "",
    order: int = 0
):
    payload = {
        "year": year,
        "title": title,
        "description": description,
        "order": order
    }
    
    response = requests.post(
        f"{API_URL}/milestones",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
