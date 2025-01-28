from openai import AsyncOpenAI
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client with error checking
openai_client = None
try:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Warning: OpenAI API key not found in environment variables")
    else:
        openai_client = AsyncOpenAI(api_key=api_key)
except Exception as e:
    print(f"Error initializing OpenAI client: {str(e)}")

async def get_gpt_response(message: str, context: Optional[str] = None, model: str = "gpt-3.5-turbo") -> str:
    try:
        if not openai_client:
            raise Exception("OpenAI client not initialized. Check your API key.")

        system_prompt = """You are a helpful AI assistant that answers questions based on the provided PDF documents. 
        If the question cannot be answered from the documents, say so clearly."""
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        if context:
            messages.append({
                "role": "system", 
                "content": f"Context from PDFs:\n{context}"
            })

        messages.append({
            "role": "user",
            "content": message
        })

        # Use gpt-3.5-turbo instead of gpt-4 for testing
        response = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # Changed from gpt-4 to gpt-3.5-turbo
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
            
    except Exception as e:
        print(f"Error in get_gpt_response: {str(e)}")  # Log the error
        raise Exception(f"OpenAI API error: {str(e)}") 