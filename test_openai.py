import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import asyncio

async def test_openai():
    try:
        # Load environment variables
        load_dotenv()
        
        # Get OpenAI key
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            print("Error: OpenAI API key not found in .env file")
            return
            
        # Test OpenAI
        client = AsyncOpenAI(api_key=openai_key)
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        print("OpenAI Response:", response.choices[0].message.content)
        print("OpenAI API Test: Success ✓")
        
    except Exception as e:
        print(f"Error testing OpenAI: {str(e)}")

# Run the test
asyncio.run(test_openai()) 