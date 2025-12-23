import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import API_URL


def read_services():
    response = requests.get(f"{API_URL}/services")
    return response.json()


def read_service_by_id(service_id: str = ""):
    response = requests.get(f"{API_URL}/services/{service_id}")
    return response.json()
