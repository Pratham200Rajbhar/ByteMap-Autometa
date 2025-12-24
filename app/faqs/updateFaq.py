import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL


def update_faq(
    faq_id: str,
    question: str = None,
    answer: str = None,
    category: str = None,
    order: int = None
):
    payload = {}
    
    if question is not None:
        payload["question"] = question
    if answer is not None:
        payload["answer"] = answer
    if category is not None:
        payload["category"] = category
    if order is not None:
        payload["order"] = order
    
    response = requests.put(
        f"{API_URL}/faqs/{faq_id}",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    return response.json()
