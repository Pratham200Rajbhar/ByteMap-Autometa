import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def update_stat(
    stat_id: str,
    label: str = None,
    value: str = None,
    icon: str = None,
    order: int = None
):
    payload = {}
    
    if label is not None:
        payload["label"] = label
    if value is not None:
        payload["value"] = value
    if icon is not None:
        payload["icon"] = icon
    if order is not None:
        payload["order"] = order
    
    response = requests.put(
        f"{API_URL}/stats/{stat_id}",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
