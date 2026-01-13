from sqlalchemy.orm import Session
from app.models.hypotheses_table import Hypotheses
from app.models.team_table import Team
from app.models.interviews_table import Interviews

def delete_team(db: Session, team_id:str):
    try:
        # relationships are set up using cascade so once a team is deleted, all associated info is also deleted
        record = db.query(Team).filter(Team.id == team_id).first() 
        if record:
            db.delete(record)
            db.commit()
            return True
        else:
            return False
        
    except Exception as e:
        db.rollback()
        return None

def delete_hypothesis(db: Session, hypothesis_id: int):
    try:
        record = db.query(Hypotheses).filter(Hypotheses.id == hypothesis_id).first()
        if record:
            db.delete(record) # delete record based on hypothesis id
            db.commit()
            return True
        else:
            return False
    
    except Exception as e:
        db.rollback()
        return None
    
def delete_interview(db: Session, interview_id: int):
    try:
        record = db.query(Interviews).filter(Interviews.id == interview_id).first()
        if record:
            db.delete(record)
            db.commit()
            return True
        else:
            return False
    except Exception as e:
        db.rollback()
        return None