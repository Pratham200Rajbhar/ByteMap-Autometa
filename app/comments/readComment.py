import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import auth_token
from config import API_URL

# Read all comments (Admin)
admin_comments_res = requests.get(
    f"{API_URL}/comments", 
    headers={"Authorization": f"Bearer {auth_token}"}
)
print("All Comments (Admin):", admin_comments_res.json())

# Example of reading comments for a specific post
blogs_response = requests.get(f"{API_URL}/blog")
if blogs_response.status_code == 200 and blogs_response.json():
    blog_id = blogs_response.json()[0].get('id')
    if blog_id:
        get_comments_res = requests.get(f"{API_URL}/comments/post/{blog_id}")
        print(f"Comments for blog {blog_id}:", get_comments_res.json())
