# Reddit Persona Chat

[![Try on Hugging Face](https://img.shields.io/badge/-HuggingFace-FDEE21?style=for-the-badge&logo=HuggingFace&logoColor=black)](https://huggingface.co/spaces/smit-faldu/Reddit-Persona-Chat) 

Reddit Persona Chat is a web application that analyzes a Reddit user's comments and posts to create a persona, which you can then chat with. The application uses LangChain and Google's Gemini model to generate realistic personas and responses.

## Features

- Analyze Reddit user activity to create detailed personas
- Chat with generated personas in a user-friendly interface
- Save persona profiles to text files
- Structured JSON output for persona traits
- Built with FastAPI for robust API endpoints
- Modern UI with responsive design
- Docker support for easy deployment
- Hugging Face Spaces compatible

## Installation

### Prerequisites

- Python 3.9+ (Python 3.10 recommended)
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Option 1: Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Reddit-Persona-Chat.git
cd Reddit-Persona-Chat
```

2. Create a virtual environment (recommended):
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Windows
copy .env.example .env
# Edit the .env file with your API keys

# Linux/Mac
cp .env.example .env
# Edit the .env file with your API keys
```

5. Start the application:
```bash
python main.py
```

6. Open your browser and navigate to:
```
http://127.0.0.1:8000
```

### Option 2: Docker Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Reddit-Persona-Chat.git
cd Reddit-Persona-Chat
```

2. Set up environment variables:
```bash
# Windows
copy .env.example .env
# Edit the .env file with your API keys

# Linux/Mac
cp .env.example .env
# Edit the .env file with your API keys
```

3. Build and run with Docker Compose:
```bash
docker-compose up -d
```

4. Open your browser and navigate to:
```
http://localhost:7860
```

### Option 3: Hugging Face Spaces Deployment

1. Fork this repository to your GitHub account

2. Create a new Hugging Face Space:
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Select "Docker" as the Space SDK
   - Connect your GitHub repository

3. Set the following environment variables in your Hugging Face Space settings:
   - `GOOGLE_API_KEY`: Your Google API key
   - `REDDIT_CLIENT_ID`: Your Reddit API client ID
   - `REDDIT_CLIENT_SECRET`: Your Reddit API client secret

## Usage

1. Enter a Reddit username in the input field and click "Generate Persona"

2. The application will analyze the user's Reddit activity and generate a persona profile

3. You can chat with the generated persona in the chat interface

4. To save the persona profile to a text file, click the "Save Persona to File" button

## How It Works

1. **Data Collection**: The application fetches the most recent comments and posts from the specified Reddit user.

2. **Persona Generation**: Using Google's Gemini AI, the application analyzes the text data to extract personality traits, habits, preferences, and other characteristics.

3. **Structured Output**: The AI generates a structured persona with fields like name, occupation, personality traits, etc.

4. **Interactive Chat**: You can then chat with an AI that adopts the persona based on the extracted traits.

5. **File Export**: You can save the generated persona to a text file for future reference.

## API Endpoints

- `GET /`: Main web interface
- `POST /api/persona`: Generate a persona from a Reddit username
- `POST /api/chat`: Chat with a generated persona
- `POST /api/save-persona`: Save a persona to a text file

## Technologies Used

- **FastAPI**: For the backend API
- **Google Gemini AI**: For text analysis and chat generation
- **LangChain**: For structured AI interactions
- **AsyncPRAW**: For asynchronous Reddit API access
- **Bootstrap**: For responsive UI
- **Docker**: For containerization and deployment

## Getting API Keys

### Google API Key
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Add it to your .env file as `GOOGLE_API_KEY`

### Reddit API Credentials
1. Go to https://www.reddit.com/prefs/apps
2. Create a new app (script type)
3. Note the client ID and client secret
4. Add them to your .env file as `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`

## License

MIT
