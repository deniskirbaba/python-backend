import requests

HOST = "localhost"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"

params = {"n": int(1e4)}
response = requests.request("GET", BASE_URL + "/fibonacci/4", params=params)
# response = requests.request("GET", BASE_URL + "/factorial", params=params)

print(f"Status code: {response.status_code}")
print(f"Response text: {response.text}")
