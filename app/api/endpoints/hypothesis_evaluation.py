from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.db.database import get_db
from app.worker.hyp_evaluation import evaluate_hypothesis_task # celery tasks that need to be called (will update as more celery tasks are created)
from app.schemas.hypothesis import HypothesisEvaluationRequest, HypothesisEvaluationResponse
from sqlalchemy.orm import Session
from celery.result import AsyncResult
from app import models


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
        hypothesis_type = hypothesis_type,
        hypothesis = hypothesis
    )
    db.add(hypothesis_addition)
    db.commit()

    # calling celery to pass on the task of evaluating the hypothesis
    task = evaluate_hypothesis_task.delay(
        hypothesis_id = hypothesis_addition.id,
        hypothesis = hypothesis_addition.hypothesis,
        hypothesis_type = hypothesis_type,
    )
    return (
        {
            "task_id" : task.id,
            "status" : "Processing",
            "hypothesis_id" : hypothesis_addition.id,
        }
    )

# route to check on the status of the hypothesis evaluation in celery
@evaluation_router.get("/status{task_id}")
async def get_status(task_id : str):
    result = AsyncResult(task_id)
    return {
        "task_id" : task_id,
        "status" : result.status,
    }
# once the processing finishes (the frontend receives a done status from the status route), it will access the database to get the results of the processing
@evaluation_router.get("/results{hypothesis_id}", response_model=HypothesisEvaluationResponse)
async def get_hypothesis_results(hypothesis_id: int, db: Session = Depends(get_db)):
    hypothesis = db.query(models.Hypotheses).filter(models.Hypotheses.id == hypothesis_id).first()
    if (hypothesis.hypotheses_output == None):
        raise HTTPException(
                status=404,
                detail= "results not found"
        )
    # the output and score will need to be set in the celery route
    return hypothesis
    
