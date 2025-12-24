import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import API_URL


def read_faqs():
    response = requests.get(f"{API_URL}/faqs")
    return response.json()


def read_faq_by_id(faq_id: str):
    response = requests.get(f"{API_URL}/faqs/{faq_id}")
    return response.json()
