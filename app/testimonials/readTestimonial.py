import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import API_URL


def read_testimonials(featured: bool = None):
    params = {}
    if featured is not None:
        params["featured"] = str(featured).lower()
    
    response = requests.get(f"{API_URL}/testimonials", params=params)
    return response.json()


def read_testimonial_by_id(testimonial_id: str):
    response = requests.get(f"{API_URL}/testimonials/{testimonial_id}")
    return response.json()
