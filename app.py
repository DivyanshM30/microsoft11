from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables (only in local development)
# On Vercel, environment variables are available directly
if os.path.exists(".env"):
    load_dotenv()

app = FastAPI(title="AI Agent - Gemini Chat")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini API
# On Vercel, environment variables are available directly via os.getenv
# Load .env file only in local development (if it exists)
if os.path.exists(".env"):
    load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not found. Please set it in Vercel environment variables or .env file")
    # Don't raise error immediately, allow health check to work

# Configure Gemini if API key is available
model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # Use the latest Gemini model (gemini-1.5-flash is faster and free tier friendly)
        # You can change to 'gemini-1.5-pro' for better quality
        # Note: gemini-2.5-flash might not exist, using gemini-1.5-flash as fallback
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
        except:
            try:
                model = genai.GenerativeModel('gemini-pro')
            except:
                logger.error("Could not initialize Gemini model")
        logger.info("Gemini API configured successfully")
    except Exception as e:
        logger.error(f"Error configuring Gemini API: {e}")
        model = None

class ChatMessage(BaseModel):
    message: str
    conversation_history: list = []

class ChatResponse(BaseModel):
    response: str
    error: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    import os
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # Try alternative path for Vercel
        try:
            with open("index.html", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="index.html not found")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Handle chat messages"""
    if not model:
        api_key_set = bool(os.getenv("GEMINI_API_KEY"))
        error_msg = "Gemini API key not configured. "
        if api_key_set:
            error_msg += "The API key is set but model initialization failed. Please check the key is valid."
        else:
            error_msg += "Please set GEMINI_API_KEY in Vercel environment variables (Settings > Environment Variables) or in .env file for local development."
        return ChatResponse(
            response="",
            error=error_msg
        )
    
    if not message.message or not message.message.strip():
        return ChatResponse(
            response="",
            error="Message cannot be empty"
        )
    
    try:
        # Convert conversation history to the format expected by Gemini
        # The history should be a list of dicts with 'role' and 'parts' keys
        history = []
        for item in message.conversation_history:
            if isinstance(item, dict) and 'role' in item and 'parts' in item:
                history.append(item)
        
        # Create a chat session with history
        chat_session = model.start_chat(history=history)
        
        # Send message and get response
        response = chat_session.send_message(message.message)
        
        return ChatResponse(
            response=response.text,
            error=None
        )
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Chat error: {error_msg}")
        # Provide more user-friendly error messages
        if "API_KEY" in error_msg or "api key" in error_msg.lower():
            error_msg = "Invalid API key. Please check your GEMINI_API_KEY in .env file"
        elif "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
            error_msg = "API quota exceeded. Please try again later."
        elif "safety" in error_msg.lower():
            error_msg = "Message was blocked by safety filters. Please rephrase your message."
        
        return ChatResponse(
            response="",
            error=error_msg
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok", 
        "service": "AI Agent",
        "gemini_configured": model is not None
    }

@app.post("/api/clear")
async def clear_history():
    """Clear conversation history endpoint"""
    return {"status": "ok", "message": "History cleared"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting AI Agent server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

