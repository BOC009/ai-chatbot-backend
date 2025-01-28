from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat

app = FastAPI(title="AI Chatbot API")

# Configure CORS with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ai-chatbot-boc009.netlify.app",
        "*"  # For development - remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(chat.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to AI Chatbot API. Use /api for endpoints."}

@app.get("/api")
async def api_root():
    return {"status": "ok", "message": "AI Chatbot API is running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return {"status": "error", "message": str(exc)} 