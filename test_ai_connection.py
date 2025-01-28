import requests
import os
from dotenv import load_dotenv

def test_ai_connection():
    # Load environment variables
    load_dotenv()
    
    # Get API token
    api_token = os.getenv('HUGGINGFACE_API_TOKEN')
    if not api_token:
        print("Error: HUGGINGFACE_API_TOKEN not found in .env file")
        return

    # API endpoint
    url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Test payload
    payload = {
        "inputs": "Hello, how are you?",
        "parameters": {
            "max_length": 100,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    try:
        print("Testing AI connection...")
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✓ Connection successful!")
        else:
            print("✗ Connection failed!")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_ai_connection() 