import asyncio
from app.api.services.ai_models import get_gpt_response

async def test():
    print("Testing AI service...")
    response = await get_gpt_response("Hello, how are you?")
    print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(test()) 