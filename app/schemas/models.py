from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class RedditUserRequest(BaseModel):
    """Request model for Reddit username"""
    username: str = Field(description="Reddit username to analyze")

class ChatRequest(BaseModel):
    """Request model for chat interaction"""
    persona: Dict[str, Any] = Field(description="Persona data")
    message: str = Field(description="User message")

class PersonaTrait(BaseModel):
    """Model for a single persona trait"""
    trait: str
    value: str
    confidence: float = Field(default=0.0, ge=0, le=1.0)

class PersonaResponse(BaseModel):
    """Response model for persona generation"""
    name: Optional[str] = None
    occupation: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    tier: Optional[str] = None
    archetype: Optional[str] = None
    personality: Optional[str] = None
    behavior: Optional[str] = None
    habits: Optional[str] = None
    goals: Optional[str] = None
    needs: Optional[str] = None
    frustrations: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None
    
    def dict(self):
        """Convert to dictionary, excluding None values"""
        return {k: v for k, v in super().model_dump().items() if v is not None}

class ChatResponse(BaseModel):
    """Response model for chat interaction"""
    response: str
    
class SavePersonaRequest(BaseModel):
    """Request model for saving persona to file"""
    username: str = Field(description="Reddit username")
    persona: Dict[str, Any] = Field(description="Persona data")