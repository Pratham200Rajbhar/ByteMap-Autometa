import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def create_faq(
    question: str = "",
    answer: str = "",
    category: str = "",
    order: int = 0
):
    payload = {
        "question": question,
        "answer": answer,
        "category": category,
        "order": order
    }
    
    response = requests.post(
        f"{API_URL}/faqs",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
