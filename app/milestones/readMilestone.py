import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import API_URL


def read_milestones():
    response = requests.get(f"{API_URL}/milestones")
    return response.json()


def read_milestone_by_id(milestone_id: str):
    response = requests.get(f"{API_URL}/milestones/{milestone_id}")
    return response.json()
