from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db.database import get_db
from app import models
from app.worker.interviewee_evaluation import evaluate_interviewee_profile # celery tasks that need to be called (will update as more celery tasks are created)
from app.schemas.interviewees import IntervieweeEvaluationBase, IntervieweeEvaluationResponse, RelevantIntervieweesList

customer_profile_router = APIRouter(
    prefix="/interviewee", tags=["customer"]
)

@customer_profile_router.post("/check_persona")
async def check_persona(data: IntervieweeEvaluationBase, db: Session = Depends(get_db)):
    team_id = data.team_id
    hypothesis = data.hypothesis
    team = db.query(models.Team).filter(models.Team.id == team_id).first()      # finds the team with the given id (uses ORM to increase compatibility with FastAPI and prevent SQL injections)

    if not team:                                                                # checks if the team is in the database
        raise HTTPException(
            status=404, 
            detail="Team not found. Please upload your hypothesis to begin"
        )

    hypothesis = db.query(models.Hypotheses).filter(model.Hypotheses.team_id == team_id and models.Hypotheses.hypothesis == hypothesis).first()
    if (hypothesis.evaluated == False):                                         # check to make sure teams have evaluated their hypothesis (so that they are not trying to find customers for a faulty hypothesis)
        raise HTTPException(
            status=404,
            detail="Please evaluate your hypothesis first"
        )
    # creating the persona and adding them to the customer profiles database: 
    new_customer_profile = models.Interviewee(
        customer_name = data.name,
        customer_industry = data.industry,
        customer_occupation = data.occupation,
        customer_experience = data.experience_level,
        team_id = team_id,
        customer_checked = False
    )
    db.add(new_customer_profile)
    db.commit()
    #db.refresh(new_customer_profile)
    # passing on the rest of the task to celery for management (task is to check whether the profile is valid by calling OpenAI)
    # assuming that the name of the celery task is "evaluate_customer_profile"
    task = evaluate_interviewee_profile.delay(
        name = data.name,
        industry = data.industry,
        occupation = data.occupation,
        experience_level = data.experience_level,
        team_id = team_id,
    )
    # returns some indication to the user (finished the route so that the API can handle concurrent requests)
    return {
        "task_id" : task.id,
        "status" : "Processing",
        "customer_id" : new_customer_profile.id,
    }

# this routes allows for "polling" of the task from the frontend. The frontend will continuously check on this task 
# in a polling loop and update the relevant frontend aspects when the status signifies that the task has finished
@customer_profile_router.get("/check_persona_status{task_id}")
async def get_status(task_id : str):
    result = AsyncResult(task_id)
    return {
        "task_id" : task_id,
        "status" : result.status,
    }

@customer_profile_router.get("/results{customer_id}", response_model=IntervieweeEvaluationResponse)
async def get_customer_results(interviewee_id: int, db: Session = Depends(get_db)):
    interviewee = db.query(models.Interviewee).filter(models.Interviewee.id == interviewee_id).first()
    if (interviewee.customers_output == None):
        raise HTTPException(
            status=404,
            detail= "results not found"
        )
    return interviewee 

# allows for the generation of sample customer_profiles to interview once a hypothesis is evaluated (this list will only be generated if the hypothesis has been evaluated to save tokens)
@customer_profile_router.get("/relevant_customers{hypothesis_id}", response_model=RelevantIntervieweesList)
async def get_relevant_customers(hypothesis_id: int, db: Session = Depends(get_db)):
    hypothesis = db.query(models.Hypotheses).filter(models.Hypotheses.id == hypothesis_id).first()
    return {
        relevant_customers : hypothesis.suggested_customer_profiles
    }







    
    
    

    
