import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL

project_data = {
    "title": "Modern E-commerce Platform",
    "category": "Web Development",
    "description": "A full-featured e-commerce platform built with Next.js and Stripe.",
    "long_description": "Detailed description of the project, including challenges faced and solutions implemented.",
    "technologies": ["Next.js", "TypeScript", "Tailwind CSS", "Stripe", "Supabase"],
    "gradient": "from-purple-600 to-indigo-600",
    "metrics": {"conversion_rate": "+25%", "load_time": "< 1s"},
    "year": "2023",
    "client_name": "Retail Corp",
    "live_url": "https://example.com",
    "github_url": "https://github.com/example/ecommerce"
}

response = requests.post(
    f"{API_URL}/projects", 
    json=project_data, 
    headers={"Authorization": f"Bearer {auth_token}"}
)

print(response.json())
