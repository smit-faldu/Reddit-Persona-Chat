from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
from typing import Optional, Dict, Any
import os
import json
from datetime import datetime
from pathlib import Path

from app.core.reddit_service import get_reddit_data
from app.core.persona_service import generate_persona, create_chat_session
from app.schemas.models import RedditUserRequest, ChatRequest, PersonaResponse, ChatResponse, SavePersonaRequest

# Set up environment variables if not already set

# Create output directory for persona files
PERSONA_DIR = Path("personas")
PERSONA_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Reddit Persona Chat")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Mount personas directory for file downloads
app.mount("/personas", StaticFiles(directory="personas"), name="personas")

# Templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/persona", response_model=PersonaResponse)
async def create_persona(user_request: RedditUserRequest):
    """Generate a persona based on Reddit user data"""
    try:
        # Get Reddit data
        comments, posts = await get_reddit_data(user_request.username)
        
        if not comments and not posts:
            raise HTTPException(status_code=404, detail=f"No data found for Reddit user: {user_request.username}")
        
        # Generate persona
        persona = await generate_persona(comments, posts)
        return persona
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_persona(chat_request: ChatRequest):
    """Chat with the generated persona"""
    try:
        response = await create_chat_session(chat_request.persona, chat_request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/save-persona")
async def save_persona_to_file(request: SavePersonaRequest):
    """Save persona to a text file"""
    try:
        # Create a filename with timestamp and username
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"persona_{request.username}_{timestamp}.txt"
        filepath = PERSONA_DIR / filename
        
        # Format the persona data
        persona_text = f"Reddit User Persona: {request.username}\n"
        persona_text += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Add each trait to the text
        for key, value in request.persona.items():
            if value and key != "raw_data":
                formatted_key = key.capitalize()
                persona_text += f"{formatted_key}: {value}\n"
        
        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(persona_text)
        
        # Return the file URL for download
        return {
            "filename": filename,
            "file_url": f"/personas/{filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save persona: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)