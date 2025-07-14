import os
import json
from typing import List, Dict, Any, Tuple, TypedDict
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.documents import Document
from app.schemas.models import PersonaResponse
from app.core.reddit_service import prepare_documents

# Configure Google Generative AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite-preview-06-17",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7,
    convert_system_message_to_human=True
)

# Define a Pydantic model for the persona traits
class PersonaTraits(BaseModel):
    name: str = Field(description="Likely first name based on content or 'Unknown'")
    occupation: str = Field(description="Likely occupation or interests")
    status: str = Field(description="Relationship or life status if mentioned")
    location: str = Field(description="Location if mentioned or 'Unknown'")
    archetype: str = Field(description="Personality archetype that best describes this person")
    personality: str = Field(description="Key personality traits")
    behavior: str = Field(description="Typical behaviors and interaction patterns")
    habits: str = Field(description="Regular habits or routines mentioned")
    goals: str = Field(description="Goals or aspirations mentioned")
    needs: str = Field(description="Psychological or emotional needs")
    frustrations: str = Field(description="Common frustrations or pain points")

# Persona generation prompt
persona_prompt_template = """
You are an expert psychologist and personality analyzer. Analyze the following Reddit posts and comments to create a detailed persona.

INSTRUCTIONS:
1. Carefully analyze the user's writing style, opinions, interests, and behaviors
2. Extract key personality traits, habits, and preferences
3. Create a comprehensive persona based on the data
4. Format your response as a structured JSON object

REDDIT DATA:
{text_data}

OUTPUT FORMAT:
{format_instructions}
"""

# Chat prompt template
chat_prompt_template = """
SYSTEM: You are now roleplaying as a persona based on the following profile. 
Respond to the user's message in character, maintaining the personality traits, speech patterns, 
and knowledge that would be consistent with this persona. Be authentic and engaging.

PERSONA PROFILE:
{persona}

USER MESSAGE: {message}
"""

async def analyze_text(documents: List[Document]) -> Dict[str, Any]:
    """Analyze text and extract persona traits"""
    combined_text = "\n---\n".join([doc.page_content for doc in documents[:50]])  # Limit to 50 documents
    
    # Create output parser
    parser = PydanticOutputParser(pydantic_object=PersonaTraits)
    
    # Create prompt
    prompt = PromptTemplate(
        template=persona_prompt_template,
        input_variables=["text_data"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # Format the prompt
    formatted_prompt = prompt.format(text_data=combined_text[:10000])  # Limit text length
    
    # Get response from LLM
    response = llm.invoke(formatted_prompt)
    
    # Parse the response
    try:
        # Extract JSON from the response
        content = response.content
        if isinstance(content, str):
            # Clean up the response to extract JSON
            json_str = content.replace("```json", "").replace("```", "").strip()
            traits = json.loads(json_str)
        else:
            traits = {}
            
        return traits
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        # Fallback with empty traits
        return {}

async def generate_persona(comments: List[str], posts: List[str]) -> PersonaResponse:
    """
    Generate a persona based on Reddit comments and posts
    
    Args:
        comments: List of user comments
        posts: List of user posts
        
    Returns:
        PersonaResponse object containing the generated persona
    """
    # Prepare documents
    documents = prepare_documents(comments, posts)
    
    # Analyze text
    try:
        traits = await analyze_text(documents)
        
        # Convert to PersonaResponse
        persona = PersonaResponse(
            name=traits.get("name", "Unknown"),
            occupation=traits.get("occupation", "Unknown"),
            status=traits.get("status", "Unknown"),
            location=traits.get("location", "Unknown"),
            archetype=traits.get("archetype", "Unknown"),
            personality=traits.get("personality", "Unknown"),
            behavior=traits.get("behavior", "Unknown"),
            habits=traits.get("habits", "Unknown"),
            goals=traits.get("goals", "Unknown"),
            needs=traits.get("needs", "Unknown"),
            frustrations=traits.get("frustrations", "Unknown")
        )
        
        return persona
    except Exception as e:
        print(f"Error generating persona: {e}")
        # Fallback with empty persona
        return PersonaResponse(
            name="Unknown",
            occupation="Unknown",
            personality="Could not determine personality traits from the available data."
        )

async def create_chat_session(persona: Dict[str, Any], message: str) -> str:
    """
    Create a chat session with the generated persona
    
    Args:
        persona: Persona data
        message: User message
        
    Returns:
        Response from the persona
    """
    # Format persona as text
    persona_text = "\n".join([f"{key}: {value}" for key, value in persona.items() if value])
    
    # Create prompt
    prompt = chat_prompt_template.format(persona=persona_text, message=message)
    
    # Get response
    response = llm.invoke(prompt)
    
    return response.content