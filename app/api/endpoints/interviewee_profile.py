from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from celery.result import AsyncResult

from app.core.db.database import get_db
from app.models.interviewees_table import Interviewees # Your specific model
from app.models.hypotheses_table import Hypotheses
from app.models.team_table import Team
from app.worker.interviewee_evaluation import evaluate_interviewee_task # Updated task name
from app.schemas.interviewees import IntervieweeEvaluationBase, IntervieweeResponse, RelevantIntervieweesList

interviewee_router = APIRouter(
    prefix="/interviewee", tags=["Interviewee"]
)

@interviewee_router.post("/check_persona", status_code=201)
async def check_persona(data: IntervieweeCreate, db: Session = Depends(get_db)):
    # 1. Validation: Does the team exist?
    team = db.query(Team).filter(Team.id == data.team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found.")

    # 2. Validation: Find the specific hypothesis and check evaluation status
    # FIX: SQLAlchemy filter needs comma or .filter() chain, not 'and'
    hypo = db.query(Hypotheses).filter(
        Hypotheses.team_id == data.team_id, 
        Hypotheses.hypothesis == data.hypothesis
    ).first()

    if not hypo:
        raise HTTPException(status_code=404, detail="Hypothesis not found.")
    
    if not hypo.evalulated: # Matching your spelling 'evalulated'
        raise HTTPException(status_code=400, detail="Please evaluate your hypothesis first.")

    # 3. Save the Interviewee "Persona"
    new_interviewee = Interviewees(
        team_id = data.team_id,
        customer_name = data.name,
        customer_industry = data.industry,
        customer_occupation = data.occupation,
        customer_experience = data.experience_level,
        customer_checked = False
    )
    
    db.add(new_interviewee)
    db.commit()
    db.refresh(new_interviewee)

    # 4. Trigger Celery to validate this persona against the hypothesis
    task = evaluate_interviewee_task.delay(
        interviewee_id = new_interviewee.id,
        hypothesis_text = hypo.hypothesis
    )

    return {
        "task_id": task.id,
        "status": "Processing",
        "interviewee_id": new_interviewee.id,
    }

@interviewee_router.get("/status/{task_id}")
async def get_status(task_id: str):
    result = AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status}

@interviewee_router.get("/results/{interviewee_id}", response_model=IntervieweeResponse)
async def get_results(interviewee_id: int, db: Session = Depends(get_db)):
    interviewee = db.query(Interviewees).filter(Interviewees.id == interviewee_id).first()
    
    if not interviewee:
        raise HTTPException(status_code=404, detail="Interviewee not found")
    
    if interviewee.customers_output is None:
        raise HTTPException(status_code=202, detail="Results are still being generated")
        
    return interviewee