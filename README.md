BT-ICORPS - Setup Guide
1. Prerequisites
Docker Desktop: Download and have it running.

Python 3.10+

Git

2. Local Environment Setup
Run these commands in order:

Bash

# Clone the repository
git clone <your-repo-url>
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
Bash

uvicorn app.main:app --reload
The API will be available at: http://localhost:8000