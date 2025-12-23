import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL

milestone_data = {
    "year": "2024",
    "title": "Expansion into AI",
    "description": "Successfully launched our AI-driven analytics suite."
}

milestone_response = requests.post(
    f"{API_URL}/milestones", 
    json=milestone_data, 
    headers={"Authorization": f"Bearer {auth_token}"}
)
print(milestone_response.json())
