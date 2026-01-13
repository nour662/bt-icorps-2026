import sys
from pathlib import Path

# Add the project root (/code) to the Python path
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

# Now these imports will work
from app.database.process_teams import process_teams
from app.core.db.database import SessionLocal
from app.models import Team, Hypotheses

def main(): 
    # 1. Start a database session
    db = SessionLocal()
    
    print("Starting team processing test...")
    
    try:
        # 2. Call your function with test data
        process_teams(
            db=db,
            team_id="UMD-2026-001",
            name="I-Corps Vector Search",
            primary_industry="Artificial Intelligence",
            secondary_industry="Data Science",
            status="active",
            password_hash="hashed_password_example"
        )
        print("Test execution finished.")
        
    except Exception as e:
        print(f"Critical error during test: {e}")
    finally:
        # 3. Always close the session
        db.close()

if __name__ == "__main__":
    main()