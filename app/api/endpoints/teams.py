from fastapi import APIRouter
from app.core.database import get_db
from app import models
from app.tasks import evaluate_interviews
from app.schemas.team import NewTeam
from .auth_helper.password_security import hash_password


users_router = APIRouter(
    prefix='/teams', tags=["Teams"]
)

@users_router.post("/sign_in")
async def authenticate_team(team_id: str, password: str, db: Session = Depends(get_db)):
    # first look for the team: 
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    if not verify_password(password, team.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect Password"
        )
    # need to provide a token here
    return {
        "message" : "Login successful"
    }

@users_router.post("create_account")
async def create_team(data: NewTeam, db: Session = Depends(get_db)):
    team = models.Team(
        id = data.team_id,
        name = data.name,
        industry = data.industry
        password_hash=hash_password(data.password)
    )
    db.add(team)
    db.commit()
    return {
        "message" = "Team created successfully"
        "status" : 200
    }
        

