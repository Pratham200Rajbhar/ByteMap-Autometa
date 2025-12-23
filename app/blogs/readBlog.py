import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import API_URL

response = requests.get(f"{API_URL}/blog")
print(response.json())
