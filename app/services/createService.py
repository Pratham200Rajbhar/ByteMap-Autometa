import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL

service_data = {
    "title": "Custom Software Development",
    "description": "Tailored software solutions designed to meet your specific business needs.",
    "icon": "Code",
    "features": ["Web Development", "Mobile Apps", "Cloud Solutions"],
    "technologies": ["React", "Node.js", "Python", "AWS"]
}

response = requests.post(
    f"{API_URL}/services", 
    json=service_data, 
    headers={"Authorization": f"Bearer {auth_token}"}
)

print(response.json())
