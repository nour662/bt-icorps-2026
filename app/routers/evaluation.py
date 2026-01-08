from fastapi import APIRouter
from pydantic import BaseModel
from .database import get_db
from . import models
from app.tasks import evaluate_hypothesis_task # celery tasks that need to be called (will update as more celery tasks are created)
from app.schemas.hypothesis import HypothesisEvaluationRequest, HypothesisEvaluationResponse

evaluation_router = APIRouter(
    prefix='/Hypothesis', tags=["Hypothesis"]
)

@evaluation_router.post("/evaluate")
async def evaluate_hypothesis(data: HypothesisEvaluationRequest, db: Session = Depends(get_db)):
    team_id = data.team_id
    hypothesis = data.hypothesis
    team = db.query(models.Team).filter(models.Team.id == team_id).first()

    if not team: 
        # adding the team to the database if this is their first time using the platform
        team = models.Team(
            id = team_id,
            name = data.name,
            industry = data.industry
            # can add new info if needed (just want to make sure we don't have to collect too much from the user)
            db.add(team)
            db.commit()
        )
     # adding the hypothesis to the database

    hypothesis_addition = models.Hypotheses(
        team_id = team_id,
        hypothesis_type = data.hypothesis_type,
        hypothesis = data.hypothesis,
        evaluated = False,
    )
    db.add(hypothesis_addition)
    db.commit()

    # calling celery to pass on the task of evaluating the hypothesis
    task = evaluate_hypothesis_task.delay(
        team_id = team_id,
        hypothesis_type = data.hypothesis_type,
        hypothesis = data.hypothesis, 
        industry = data.industry
    )
    return (
        "task_id" : task.id,
        "status" : "Processing",
        "hypothesis_id" : hypothesis_addition.id,
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
    
