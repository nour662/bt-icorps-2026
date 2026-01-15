from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.db.database import get_db
from app.worker.hyp_evaluation import evaluate_hypothesis_task # celery tasks that need to be called (will update as more celery tasks are created)
from app.schemas.hypothesis import HypothesisEvaluationRequest, HypothesisEvaluationResponse, HypothesisDropdown
from sqlalchemy.orm import Session
from celery.result import AsyncResult
from app import models
from app.core.celery_app import celery_app


evaluation_router = APIRouter(
    prefix='/hypothesis', tags=["Hypothesis"]
)

@evaluation_router.post("/evaluate")
async def evaluate_hypothesis(data: HypothesisEvaluationRequest, db: Session = Depends(get_db)):
    team_id = data.team_id # will later be decoded using a token
    hypothesis_type = data.hypothesis_type
    hypothesis = data.hypothesis
    
    # adding the hypothesis to the database

    hypothesis_addition = models.Hypotheses(
        team_id = team_id,
        hyp_type = hypothesis_type,
        hypothesis = hypothesis
    )
    db.add(hypothesis_addition)
    db.commit()

    # calling celery to pass on the task of evaluating the hypothesis
    task = evaluate_hypothesis_task.delay(
        hypothesis_id = hypothesis_addition.id,
        hypothesis_text = hypothesis_addition.hypothesis,
        hypothesis_type = hypothesis_type,
        team_id = team_id
    )
    return (
        {
            "task_id" : task.id,
            "status" : "Processing",
            "hypothesis_id" : hypothesis_addition.id,
        }
    )

# route to check on the status of the hypothesis evaluation in celery
@evaluation_router.get("/status/{task_id}")
async def get_status(task_id : str):
    result = celery_app.AsyncResult(task_id)
    return {
        "task_id" : task_id,
        "status" : result.status,
    }
# once the processing finishes (the frontend receives a done status from the status route), it will access the database to get the results of the processing
@evaluation_router.get("/results/{hypothesis_id}", response_model=HypothesisEvaluationResponse)
async def get_hypothesis_results(hypothesis_id: int, db: Session = Depends(get_db)):
    hypothesis = db.query(models.Hypotheses).filter(models.Hypotheses.id == hypothesis_id).first()
    if (hypothesis):
        print("\napi success\n")
    else:
        raise HTTPException(
                status_code=404,
                detail= "hypothesis DNE"
        )
    if (hypothesis.hypotheses_output == None):
        raise HTTPException(
                status_code=202,
                detail= "results not found"
        )
    # the output and score will need to be set in the celery route
    return {
        "hypotheses_output" : hypothesis.hypotheses_output,
        "hypotheses_output_score" : hypothesis.hypotheses_output_score
    }
    

@evaluation_router.get("/dropdown", response_model=List[HypothesisDropdown]) # only send id and text and transform to JSON
async def get_hypotheses_for_dropdown(db: Session = Depends(get_db), team_id : int):
    results = db.query(models.Hypotheses).filter(
        models.Hypotheses.team_id == team.id
    ).all()
    
    return results