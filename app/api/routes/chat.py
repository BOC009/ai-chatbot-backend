from fastapi import APIRouter, HTTPException, UploadFile, File, status
from pydantic import BaseModel
from typing import List, Optional
import traceback
from app.api.services.pdf_processor import process_pdf
from app.api.services.ai_models import get_gpt_response, AIAssistant

router = APIRouter()

class Message(BaseModel):
    text: str
    files: List[str]
    model: str

class ChatResponse(BaseModel):
    response: str
    error: Optional[str] = None
    status: str = "success"

# Store PDF contents in memory
pdf_contents = {}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Check file size (10MB limit)
        file_size = 0
        content = await file.read()
        file_size = len(content)
        await file.seek(0)  # Reset file pointer
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large. Maximum size is 10MB"
            )

        # Check file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed"
            )

        # Process the file
        content = await process_pdf(file)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract text from PDF"
            )

        # Store the content
        pdf_contents[file.filename] = content
        return {"message": "File processed successfully"}

    except Exception as e:
        print(f"Upload Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: Message):
    try:
        print(f"\n=== New Chat Request ===")
        print(f"Message: {message.text}")
        print(f"Files: {message.files}")
        
        # Get context from PDFs if available
        context = ""
        if message.files:
            for filename in message.files:
                if filename in pdf_contents:
                    context += pdf_contents[filename] + "\n"
                else:
                    print(f"Warning: File not found - {filename}")

        # Get response from AI
        response = await get_gpt_response(
            message=message.text,
            context=context if context else None
        )
        
        print(f"AI Response: {response}")
        return ChatResponse(response=response)
        
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"Error in chat_endpoint: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        return ChatResponse(
            response="An error occurred",
            error=error_msg,
            status="error"
        )

@router.get("/learning-status")
async def get_learning_status():
    try:
        assistant = AIAssistant()
        return assistant.get_learning_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 