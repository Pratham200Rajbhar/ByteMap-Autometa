import requests
from config import API_URL

contact_data = {
    "name": "John Smith",
    "email": "john@example.com",
    "company": "Design Pro",
    "budget": "$5k - $10k",
    "message": "I'm interested in a new website for my design agency."
}

post_response = requests.post(f"{API_URL}/contact", json=contact_data)
print(post_response.status_code)
