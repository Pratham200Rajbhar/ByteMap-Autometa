import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL

faq_data = {
    "question": "What is your typical project timeline?",
    "answer": "Most projects are completed within 4-12 weeks depending on complexity.",
    "category": "General"
}

response = requests.post(
    f"{API_URL}/faqs", 
    json=faq_data, 
    headers={"Authorization": f"Bearer {auth_token}"}
)

print(response.json())
