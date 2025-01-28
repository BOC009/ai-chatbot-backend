import asyncio
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI

async def test_setup():
    try:
        # Load environment variables
        load_dotenv()
        
        # Check API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("Error: OPENAI_API_KEY not found in .env file")
            return
            
        print("API Key found:", api_key[:10] + "..." + api_key[-5:])
        
        # Test API connection
        client = AsyncOpenAI(api_key=api_key)
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            max_tokens=50
        )
        
        print("\nAPI Test Response:", response.choices[0].message.content)
        print("\nSetup test successful! ✓")
        
    except Exception as e:
        print(f"\nError during setup test: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_setup()) 