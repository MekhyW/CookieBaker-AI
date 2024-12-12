import requests

def make_get_request():
    url = 'http://localhost:5678/webhook-test/logs/error'
    
    params = {
        "prompt": "Isso não é uma piada",
        "chat_id": "chat123",
        "client_name": "test_client",
        "sfw": True,
        "sender_name": "Felipe Catapano",
        "media": ""
    }

    response = requests.get(url, params=params)

    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.text}")

if __name__ == "__main__":
    make_get_request()
