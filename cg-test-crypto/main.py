# Gate 2: Cryptography & TLS Gate
import hashlib
import requests

def hash_data(data):
    # Weak hash algorithm
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    return m.hexdigest()

def fetch_data():
    # TLS verification disabled
    response = requests.get('http://api.example.com/data', verify=False)
    return response.text

if __name__ == '__main__':
    print(hash_data("secret_info"))
    fetch_data()
