import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def update_contact(
    contact_id: str,
    is_read: bool = None,
    status: str = None
):
    payload = {}
    
    if is_read is not None:
        payload["is_read"] = is_read
    if status is not None:
        payload["status"] = status
    
    response = requests.put(
        f"{API_URL}/contact/{contact_id}",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
