from sqlalchemy.orm import Session
from app.core.db.database import SessionLocal, engine
from app.models.team_table import Team  

def process_teams(db: Session, team_id: str, name: str, 
                 primary_industry: str, secondary_industry: str, 
                 status:str, password_hash:str):

    # creating database object
    new_team = Team(
        id = team_id,
        name = name,
        primary_industry = primary_industry,
        secondary_industry = secondary_industry,
        status = status,
        password_hash = password_hash # hash for security
    )
    
    try:
        db.merge(new_team) # merge in case of duplicates 
        # (alternatively could create check for duplicates before executing code)
        db.commit()
        print(f"Successfully created team: {new_team.name}") # print statements for debug
        print(f"Team ID: {new_team.team_id}")    
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

