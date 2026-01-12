from sqlalchemy.orm import Session
from app.models.hypotheses_table import Hypotheses

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