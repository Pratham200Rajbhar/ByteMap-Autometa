import requests
from config import API_URL

get_response = requests.get(f"{API_URL}/milestones")
print(get_response.json())
