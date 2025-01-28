import requests
import asyncio

def test_model():
    print("Testing AI model...")
    
    url = "https://api-inference.huggingface.co/models/EleutherAI/gpt2-medium"
    
    payload = {
        "inputs": "Question: What is Python?\nAnswer:",
        "parameters": {
            "max_length": 100,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    try:
        print("Sending request...")
        response = requests.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✓ Test successful!")
        else:
            print("✗ Test failed!")
            
    except Exception as e:
        print(f"Error: {str(e)}")

async def test_chat():
    from app.api.services.ai_models import get_gpt_response
    
    try:
        response = await get_gpt_response("Hello")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_model()
    asyncio.run(test_chat()) 