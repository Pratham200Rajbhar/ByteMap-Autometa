import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def update_milestone(
    milestone_id: str,
    year: str = None,
    title: str = None,
    description: str = None,
    order: int = None
):
    payload = {}
    
    if year is not None:
        payload["year"] = year
    if title is not None:
        payload["title"] = title
    if description is not None:
        payload["description"] = description
    if order is not None:
        payload["order"] = order
    
    response = requests.put(
        f"{API_URL}/milestones/{milestone_id}",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
