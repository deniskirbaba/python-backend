import requests

HOST = "localhost"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"

params = {"aan": ["as", "bb"], "n": 10}
response = requests.request("GET", BASE_URL + "/factorial", params=params)

print(f"Status code: {response.status_code}")
print(f"Response text: {response.text}")
