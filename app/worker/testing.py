import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.core.celery_app import celery_app

from celery import Celery
from app.core.database import SessionLocal, engine, Base
from app.database.process_teams import process_team
from app.database.process_interviews import process_interview
from app.database.process_input_hypothesis import save_hypothesis

from app.core.celery_app import celery_app


# 2. The Background Task

@celery_app.task(name="tasks.testing")

def populate_research_chain(team, interview, hypothesis):
    """
    Background worker task to handle the DB commits and OpenAI Embeddings.
    """
    db = SessionLocal()
    try:
        print(f"--- Worker: Processing Team {team['name']} ---")
        process_team(db, **team)

        print(f"--- Worker: Logging Interview for {interview['interviewee_name']} ---")
        # Ensure the interview is linked to the correct team_id
        interview['team_id'] = team['team_id']
        process_interview(db, **interview)

        print(f"--- Worker: Generating Embedding & Saving Hypothesis ---")
        # Ensure hypothesis is linked to the team_id
        hypothesis['team_id'] = team['team_id']
        save_hypothesis(db, **hypothesis)

        return {"status": "Complete", "team_id": team['team_id']}
    except Exception as e:
        print(f"Worker Error: {str(e)}")
        return {"status": "Failed", "error": str(e)}
    finally:
        db.close()

# 3. The Main Trigger (The Producer)
def run_production_sample():
    """
    Initializes the DB and sends the work to the Celery queue.
    """
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Prepare Data
    t_id = f"TEAM-{uuid.uuid4().hex[:6].upper()}"
    
    team_data = {
        "team_id": t_id,
        "name": "UMD Sprinternship Team",
        "primary_industry": "Education",
        "secondary_industry": "Tech",
        "status": "active",
        "passcode": "terps2026"
    }

    interview_data = {
        "interviewee_name": "Bobby Smith",
        "s3_key": f"s3://bucket/interviews/{t_id}_bobby.pdf"
    }

    hypothesis_data = {
        "hypothesis_input": "Automated transcription improves data accuracy in research.",
        "h_type": "Efficiency"
    }

    print(f"🚀 Dispatching population task for {t_id} to Redis...")
    
    # .delay() sends it to the worker
    task = populate_research_chain.delay(team_data, interview_data, hypothesis_data)
    
    print(f"✅ Task queued! Task ID: {task.id}")
    print("Check worker logs to see the actual database commits.")

if __name__ == "__main__":
    run_production_sample()