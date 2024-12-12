import requests

def make_get_request():
    url = 'http://localhost:5678/webhook-test/response'
    
    params = {
        "prompt": "What is this?",
        "chat_id": "chat123",
        "client_name": "test_client",
        "sfw": True,
        "sender_name": "Felipe Catapano",
        "media": "https://cdn.awsli.com.br/600x1000/519/519712/produto/38217083/3cfa6a6c1e.jpg"
    }

    response = requests.get(url, params=params)

    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.text}")

if __name__ == "__main__":
    make_get_request()
