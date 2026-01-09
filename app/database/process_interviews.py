from sqlalchemy.orm import Session
from app.models.interviews_table import Interviews # Ensure this matches your file name

def process_interview(db: Session, 
                      team_id: str, 
                      interviewee_name: str, 
                      s3_key: str):
    
    # Creating the database object
    new_interview = Interviews(
        team_id = team_id,
        interviewee_name = interviewee_name,
        s3_key = s3_key,
        interviews_output = "" # update with ai analysis later
    )
    
    try:
        # add to session
        db.add(new_interview)
        db.commit()
        
        db.refresh(new_interview) # ensures that info is up to date
        
        # print statements for debugging:
        print(f"Interview Logged: {new_interview.interviewee_name}") 
        print(f"ID: {new_interview.id} | S3 Path: {new_interview.s3_key}")
        return new_interview
        
    except Exception as e:
        db.rollback()
        print(f"error: {e}")
        return None