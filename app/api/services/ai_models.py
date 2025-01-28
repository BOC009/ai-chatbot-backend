import aiohttp
from typing import Optional, Dict
import asyncio
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIAssistant:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/facebook/opt-1.3b"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_TOKEN')}",
            "Content-Type": "application/json"
        }
        self.conversation_history = []

    async def get_response(self, message: str) -> str:
        try:
            # Format prompt with conversation history
            prompt = self._format_prompt(message)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=self.headers,
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "max_length": 100,
                            "temperature": 0.7,
                            "return_full_text": False
                        }
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result[0]["generated_text"]
                    else:
                        return "I apologize, but I'm having trouble generating a response."
            
        except Exception as e:
            print(f"Error in get_response: {str(e)}")
            return "I encountered an error. Please try again."

    def _format_prompt(self, message: str) -> str:
        return f"Question: {message}\nAnswer:"

async def get_gpt_response(message: str, context: Optional[str] = None) -> str:
    try:
        assistant = AIAssistant()
        if context:
            message = f"Context: {context}\n\nQuestion: {message}"
        response = await assistant.get_response(message)
        return response
    except Exception as e:
        print(f"Error in get_gpt_response: {str(e)}")
        return "I encountered an error. Please try again." 