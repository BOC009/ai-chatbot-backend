import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import google.generativeai as genai

# Create this test file
async def test_api_keys():
    try:
        # Load environment variables
        load_dotenv()
        
        # Test OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        print(f"OpenAI API Key found: {'✓' if openai_key else '✗'}")
        if openai_key:
            client = AsyncOpenAI(api_key=openai_key)
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            print("OpenAI API Test: ✓")
        
        # Test Anthropic
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        print(f"Anthropic API Key found: {'✓' if anthropic_key else '✗'}")
        if anthropic_key:
            client = AsyncAnthropic(api_key=anthropic_key)
            response = await client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=5,
                messages=[{"role": "user", "content": "Hello"}]
            )
            print("Anthropic API Test: ✓")
        
        # Test Google
        google_key = os.getenv('GOOGLE_API_KEY')
        print(f"Google API Key found: {'✓' if google_key else '✗'}")
        if google_key:
            genai.configure(api_key=google_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Hello")
            print("Google API Test: ✓")
            
    except Exception as e:
        print(f"Error: {str(e)}")

# Run the test
import asyncio
asyncio.run(test_api_keys()) 