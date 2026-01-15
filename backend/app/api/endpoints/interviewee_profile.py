from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from celery.result import AsyncResult

from app.core.db.database import get_db
from app.models.interviewees_table import Interviewees # Your specific model
from app.models.ai_interviewees_table import AI_Interviewees
from app.models.hypotheses_table import Hypotheses
from app.models.team_table import Team
from app.worker.interviewee_evaluation import evaluate_interviewee_profile # Updated task name
from app.worker.user_interviewee_evaluation import evaluate_interviewee_task
from app.schemas.interviewees import IntervieweeEvaluationBase, IntervieweeEvaluationResponse, RelevantIntervieweesList

interviewee_router = APIRouter(
    prefix="/interviewee", tags=["Interviewee"]
)

@interviewee_router.post("/check_persona")
async def check_persona(data: IntervieweeEvaluationBase, db: Session = Depends(get_db)):
    # 1. Validation: Does the team exist?
    # team = db.query(Team).filter(Team.id == data.team_id).first()
    # if not team:
    #     raise HTTPException(status_code=404, detail="Team not found.")

    # 2. Validation: Find the specific hypothesis and check evaluation status
    hypo = db.query(Hypotheses).filter(
        Hypotheses.team_id == data.team_id, 
        Hypotheses.id == data.hypothesis_id
    ).first()

    if not hypo:
        raise HTTPException(status_code=404, detail="Hypothesis not found.")
    
    # if not hypo.evaluated: 
    #     raise HTTPException(status_code=400, detail="Please evaluate your hypothesis first.")

    # 3. Save the Interviewee "Persona"
    new_interviewee = Interviewees(
        team_id = data.team_id,
        customer_name = data.name, # Maps 'name' from JSON to 'customer_name' in DB
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

@interviewee_router.get("/results/{interviewee_id}", response_model=IntervieweeEvaluationResponse)
async def get_results(interviewee_id: int, db: Session = Depends(get_db)):
    interviewee = db.query(Interviewees).filter(Interviewees.id == interviewee_id).first()
    
    if not interviewee:
        raise HTTPException(status_code=404, detail="Interviewee not found")
    
    if interviewee.customers_output is None:
        raise HTTPException(status_code=202, detail="Results are still being generated")
        
    return {
        "id": interviewee.id,
        "team_id": interviewee.team_id,
        "customer_name": interviewee.customer_name,
        "industry": interviewee.customer_industry,    
        "occupation": interviewee.customer_occupation, 
        "experience_level": interviewee.customer_experience, 
        "customer_checked": interviewee.customer_checked,
        "customers_output": interviewee.customers_output,
        "customers_output_score": interviewee.customers_output_score
    }

@interviewee_router.get("/generate_relevant_personas/{hypothesis_id}")
async def get_relevant_customers(hypothesis_id: int, db: Session = Depends(get_db)):
    hypo = db.query(Hypotheses).filter(Hypotheses.id == hypothesis_id).first()
    if not hypo:
        raise HTTPException(status_code=404, detail="Hypothesis not found.")
    
    # 
    task = evaluate_interviewee_profile.delay(hypothesis_id=hypothesis_id)
    return {
        "task_id": task.id,
        "status": "Generating ideal personas...",
        "hypothesis_id": hypothesis_id
    }
    
    
@interviewee_router.get("/relevant_interviewees/{hypothesis_id}", response_model=RelevantIntervieweesList)
async def get_relevant_customers(hypothesis_id: int, db: Session = Depends(get_db)):
    """Returns the list of AI-suggested personas from the database."""
    
    suggestions = db.query(AI_Interviewees).filter(
        AI_Interviewees.hypothesis_id == hypothesis_id
    ).all()
    
    if not suggestions:
        return {"relevant_customers": []}
        
    return {"relevant_customers": suggestions}