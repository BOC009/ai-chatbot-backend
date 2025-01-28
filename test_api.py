import asyncio
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

async def test_api():
    try:
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print("Error: No API key found in .env file")
            return
            
        client = AsyncOpenAI(api_key=api_key)
        
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        print("API Test Successful!")
        print("Response:", response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error testing API: {str(e)}")

# Run the test
asyncio.run(test_api()) 