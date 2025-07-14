import uvicorn
import os
import sys
from pathlib import Path

# Ensure the app directory exists
app_dir = Path("app")
static_dir = app_dir / "static"
css_dir = static_dir / "css"
js_dir = static_dir / "js"
templates_dir = app_dir / "templates"

# Create directories if they don't exist
for directory in [app_dir, static_dir, css_dir, js_dir, templates_dir]:
    directory.mkdir(exist_ok=True)

if __name__ == "__main__":
    
    # Run the application
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)