import requests
from config import API_URL

blogs_response = requests.get(f"{API_URL}/blog")
if blogs_response.status_code == 200 and blogs_response.json():
    blog_id = blogs_response.json()[0].get('id')
    
    if blog_id:
        comment_data = {
            "blog_post_id": blog_id,
            "author_name": "Reviewer X",
            "content": "This is a great article! Very informative."
        }
        post_comment_res = requests.post(f"{API_URL}/comments", json=comment_data)
        print(post_comment_res.json())
