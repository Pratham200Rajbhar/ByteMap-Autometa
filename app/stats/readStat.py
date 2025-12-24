import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import API_URL


def read_stats():
    response = requests.get(f"{API_URL}/stats")
    return response.json()


def read_stat_by_id(stat_id: str):
    response = requests.get(f"{API_URL}/stats/{stat_id}")
    return response.json()
