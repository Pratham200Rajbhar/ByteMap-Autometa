import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import API_URL


def read_projects():
    response = requests.get(f"{API_URL}/projects")
    return response.json()


def read_project_by_id(project_id: str = ""):
    response = requests.get(f"{API_URL}/projects/{project_id}")
    return response.json()


def read_project_by_slug(slug: str = ""):
    response = requests.get(f"{API_URL}/projects/slug/{slug}")
    return response.json()
