BT-ICORPS - Setup Guide
1. Prerequisites
Docker Desktop: Download and have it running.

Python 3.10+

Git

2. Local Environment Setup
Run these commands in order:

Bash

# Clone the repository
git clone https://github.com/nour662/bt-icorps-2026.git
cd BT-ICORPS-2026

# Create and activate virtual environment (in project root folder)
python -m venv .venv
# On Mac
source .venv/bin/activate  
# Windows: 
.venv\Scripts\Activate 

# Install dependencies
pip install -r requirements.txt

# Setup secrets
cp .env.example .env


3. Launch Infrastructure
This starts the Database (Postgres), Cache (Redis), and Storage (MinIO):

Bash

docker compose up -d

4. Run the Application
To run the full system, you need two terminal tabs open:

Terminal 1: The API (Uvicorn)
This handles the web requests and the documentation.

Bash

uvicorn app.main:app --reload
API URL: http://localhost:8000

Interactive Docs: http://localhost:8000/docs

Terminal 2: The AI Worker (Celery)
This handles the heavy "Linear Chain" AI processing in the background.

Bash

celery -A app.core.celery_app worker --loglevel=info
5. Verify Your Setup
Once both terminals are running, visit the Health Check to ensure the Python code is talking to Docker correctly:

Check Health: http://localhost:8000/health

Success looks like this:

JSON

{
  "database": "connected",
  "redis": "connected",
  "environment": "development"
}