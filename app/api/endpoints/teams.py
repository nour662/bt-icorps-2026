from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db.database import get_db
from app import models
#from app.worker import evaluate_interviews
from app.schemas.team import NewTeam, TeamLogin
from .auth_helper.password_security import hash_password, verify_password
from .auth_helper.auth import create_access_token

teams_router = APIRouter(
    prefix='/teams', tags=["Teams"]
)

@teams_router.post("/sign_in")
async def authenticate_team(data: TeamLogin, db: Session = Depends(get_db)):
    # first look for the team: 
    team_id = data.team_id
    password = data.password
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
    token = create_access_token(team_id)
    return {
        "message" : "Login successful",
        "access_token" : token,
        "token_type" : "bearer"
    }

@teams_router.post("/create_account")
async def create_team(data: NewTeam, db: Session = Depends(get_db)):
    team = models.Team(
        id = data.team_id,
        name = data.team_name,
        industry = data.industry,
        password_hash=hash_password(data.password)
    )
    db.add(team)
    db.commit()
    return {
        "message" : "Team created successfully",
        "status" : 200
    }


        

