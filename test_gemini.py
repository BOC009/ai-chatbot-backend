import os
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio

async def test_gemini():
    try:
        # Load environment variables
        load_dotenv()
        
        # Get API key
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("Error: GOOGLE_API_KEY not found in .env file")
            return
            
        print(f"API Key found: {api_key[:10]}...")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Initialize model
        model = genai.GenerativeModel('gemini-pro')
        
        # Test response
        response = model.generate_content("Say hello!")
        
        print("\nGemini Response:", response.text)
        print("\nTest successful! ✓")
        
    except Exception as e:
        print(f"\nError testing Gemini: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_gemini()) 