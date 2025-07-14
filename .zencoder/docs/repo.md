# Reddit Persona Chat

## Summary
Reddit Persona Chat is a web application that analyzes Reddit user activity to create detailed personas, which users can then chat with. The application uses LangChain and Google's Gemini model to generate realistic personas and responses based on a user's Reddit comments and posts.

## Structure
- **app/**: Main application code
  - **api/**: API endpoints
  - **core/**: Core services (Reddit data fetching, persona generation)
  - **schemas/**: Data models
  - **static/**: Static assets (CSS, JavaScript)
  - **templates/**: HTML templates
- **personas/**: Directory for saved persona files
- **main.py**: Application entry point

## Language & Runtime
**Language**: Python
**Version**: Python 3.9+ (3.10 recommended)
**Framework**: FastAPI
**Package Manager**: pip

## Dependencies
**Main Dependencies**:
- fastapi: Web framework for building APIs
- uvicorn: ASGI server for FastAPI
- asyncpraw: Asynchronous Reddit API wrapper
- google-generativeai: Google Gemini AI API
- langchain: Framework for LLM applications
- langchain-google-genai: LangChain integration with Google Generative AI
- langchain-text-splitters: Text splitting utilities
- langgraph: Orchestration for LLM applications
- pydantic: Data validation and settings management
- jinja2: Template engine for HTML

## Build & Installation
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with API keys

# Start the application
python main.py
```

## Docker
**Dockerfile**: Dockerfile
**Image**: Python 3.10-slim based image
**Configuration**: 
- First installs requirements as wheels
- Creates a new environment
- Uses the installed wheels in the new environment
- Exposes port 7860, mounts personas directory
**Run Command**:
```bash
docker-compose up -d
```

## Main Files
**Entry Point**: main.py
**Application**: app/main.py
**Services**:
- app/core/reddit_service.py: Fetches Reddit user data
- app/core/persona_service.py: Generates personas and handles chat

## API Endpoints
- `GET /`: Main web interface
- `POST /api/persona`: Generate a persona from a Reddit username
- `POST /api/chat`: Chat with a generated persona
- `POST /api/save-persona`: Save a persona to a text file

## Environment Variables
**Required**:
- GOOGLE_API_KEY: Google API key for Gemini model
- REDDIT_CLIENT_ID: Reddit API client ID
- REDDIT_CLIENT_SECRET: Reddit API client secret
- REDDIT_USER_AGENT: User agent for Reddit API (default: "persona-script")