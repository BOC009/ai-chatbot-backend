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
        # Using a more reliable model
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_TOKEN')}",
            "Content-Type": "application/json"
        }
        self.conversation_history = []

    async def get_response(self, message: str) -> str:
        try:
            prompt = self._format_prompt(message)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=self.headers,
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "max_length": 150,
                            "temperature": 0.7,
                            "return_full_text": False
                        }
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        print("API Response:", result)  # Debug print
                        return result[0]["generated_text"]
                    else:
                        error_text = await response.text()
                        print(f"API Error: Status {response.status}, {error_text}")  # Debug print
                        return "I apologize, but I'm having trouble generating a response."
            
        except Exception as e:
            print(f"Error in get_response: {str(e)}")  # Debug print
            return "I encountered an error. Please try again."

    def _format_prompt(self, message: str) -> str:
        return f"Human: {message}\nAssistant:"

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