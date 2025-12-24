import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def create_stat(
    label: str = "",
    value: str = "",
    icon: str = "",
    order: int = 0
):
    payload = {
        "label": label,
        "value": value,
        "icon": icon,
        "order": order
    }
    
    response = requests.post(
        f"{API_URL}/stats",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
