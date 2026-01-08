from fastapi import APIRouter
from app.core.database import get_db
from . import models
from app.tasks import validate_profile_task # celery tasks that need to be called (will update as more celery tasks are created)
from app.schemas.customer import CustomerEvaluationBase, CustomerEvaluationResponse

customer_profile_router = APIRouter(
    prefix="/customer", tags=["customer"]
)

@customer_profile_router.post("/check_persona")
async def check_persona(data: CustomerEvaluationBase, db: Session = Depends(get_db)):
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
    new_customer_profile = models.Customer(
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
    task = evaluate_customer_profile.delay(
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

    @customer_profile_router.get("/results{customer_id}", response_model=CustomerEvaluationResponse)
    async def get_customer_results(customer_id: int, db: Session = Depends(get_db)):
        customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
        if (customer.customers_output == None):
            raise HTTPException(
                status=404,
                detail= "results not found"
            )
        return customer 







    
    
    

    
