import requests
import json

def test_chat():
    url = "http://localhost:8000/api/chat"
    
    payload = {
        "text": "Hello, how are you?",
        "files": [],
        "model": "free-chat"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_chat() 