import requests
from config import API_URL

get_response = requests.get(f"{API_URL}/projects")
print(get_response.json())
