import google.generativeai as genai
from typing import Optional, Dict
import asyncio
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google AI
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Initialize Gemini
genai.configure(api_key=api_key)

# Configure model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Create global model instance
model = genai.GenerativeModel(
    model_name='gemini-pro',
    generation_config=generation_config,
    safety_settings=safety_settings
)

class AIAssistant:
    def __init__(self):
        self.chat = model.start_chat(history=[])
        self.learning_status = {
            "status": {
                "last_updated": datetime.datetime.now().isoformat(),
                "total_facts": 0,
                "recent_learnings": [],
                "categories": {
                    "general": 0,
                    "science": 0,
                    "technology": 0,
                    "math": 0
                }
            },
            "knowledge_base_size": 0,
            "learned_responses_count": 0,
            "categories": ["general", "science", "technology", "math"]
        }

    def get_learning_status(self) -> Dict:
        return self.learning_status

    def _update_learning_status(self, category: str, fact: str):
        now = datetime.datetime.now().isoformat()
        self.learning_status["status"]["last_updated"] = now
        self.learning_status["status"]["total_facts"] += 1
        
        if category in self.learning_status["status"]["categories"]:
            self.learning_status["status"]["categories"][category] += 1
        else:
            self.learning_status["status"]["categories"][category] = 1

        self.learning_status["status"]["recent_learnings"].insert(0, {
            "time": now,
            "category": category,
            "fact": fact
        })
        
        self.learning_status["status"]["recent_learnings"] = \
            self.learning_status["status"]["recent_learnings"][:10]
        self.learning_status["learned_responses_count"] += 1
        self.learning_status["knowledge_base_size"] += 1

    async def get_response(self, message: str) -> str:
        try:
            # Add system prompt to guide the model
            system_prompt = """You are a helpful, intelligent AI assistant. 
            Provide clear, accurate, and informative responses. 
            If you're not sure about something, say so honestly.
            Always maintain a friendly and professional tone."""
            
            # Prepare the message with the system prompt
            full_message = f"{system_prompt}\n\nUser: {message}\nAssistant:"
            
            # Get response from model
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.chat.send_message(full_message, stream=False)
            )
            
            # Update learning status
            self._update_learning_status("general", f"Q: {message}")
            
            # Return the response text
            return response.text
            
        except Exception as e:
            print(f"Error in get_response: {str(e)}")
            # Try direct generation as fallback
            try:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: model.generate_content(message)
                )
                return response.text
            except:
                return "I apologize, but I'm having trouble at the moment. Please try asking your question again."

async def get_gpt_response(message: str, context: Optional[str] = None, model: str = "free-chat") -> str:
    try:
        assistant = AIAssistant()
        if context:
            message = f"Context: {context}\n\nQuestion: {message}"
        response = await assistant.get_response(message)
        return response
    except Exception as e:
        print(f"Error in get_gpt_response: {str(e)}")
        return "I encountered an error. Please try again." 