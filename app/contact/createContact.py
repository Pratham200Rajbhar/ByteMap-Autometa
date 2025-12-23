import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import API_URL


def create_contact(
    name: str = "",
    email: str = "",
    company: str = "",
    budget: str = "",
    message: str = ""
):
    payload = {
        "name": name,
        "email": email,
        "company": company,
        "budget": budget,
        "message": message
    }
    
    response = requests.post(f"{API_URL}/contact", json=payload)
    return response.json()
