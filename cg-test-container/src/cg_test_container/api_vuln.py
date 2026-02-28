import requests

def make_request():
    response = requests.get("https://example.com", verify=False)
    return response.content
