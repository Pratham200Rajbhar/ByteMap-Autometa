import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL

stat_data = {
    "label": "Projects Completed",
    "value": "150+",
    "icon": "CheckCircle"
}

stat_response = requests.post(
    f"{API_URL}/stats", 
    json=stat_data, 
    headers={"Authorization": f"Bearer {auth_token}"}
)
print(stat_response.json())
