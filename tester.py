import requests

url = "http://127.0.0.1:8000/api/v1/login/"
token = "32d9436af62655bf9bbf15752fe80f38ba2f0a37"
# response = requests.post(url, data={"username": "alisher", "password": "alidev2005"})
response = requests.get(
    url="http://127.0.0.1:8000/api/v1/profiles/",
    headers={"Authorization": f"Token {token}"}
)
print(response.text)