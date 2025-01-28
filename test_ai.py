import asyncio
from app.api.services.ai_models import get_gpt_response

async def test_ai():
    print("Testing AI service...")
    
    # Test simple question
    question = "What is 2+2?"
    print(f"\nTesting question: {question}")
    response = await get_gpt_response(question)
    print(f"Response: {response}")
    
    # Test with context
    context = "The sky is blue because of Rayleigh scattering."
    question = "Why is the sky blue?"
    print(f"\nTesting question with context: {question}")
    response = await get_gpt_response(question, context)
    print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(test_ai()) 