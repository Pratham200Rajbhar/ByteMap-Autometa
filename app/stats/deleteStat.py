import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def delete_stat(stat_id: str):
    response = requests.delete(
        f"{API_URL}/stats/{stat_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
