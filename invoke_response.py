import requests

def make_get_request():
    # Define the base URL
    url = 'http://localhost:5678/webhook-test/response'
    
    # Define the test parameters
    params = {
        'sfw': True,
        'chat_title': 'Test Chat',
        'chat_description': 'This is a test chat description',
        'prompt': 'Test prompt for chatbot',
        'sender_name': 'Test User',
        'sender_isadmin': False,
        'media': ''
    }

    # Make the GET request
    response = requests.get(url, params=params)

    # Print the response
    if response.status_code == 200:
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
    else:
        print(f"Failed to reach the webhook. Status Code: {response.status_code}")

if __name__ == "__main__":
    make_get_request()
