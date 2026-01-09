from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session 

from .auth import decode_access_token
from app.core.database import get_db
from app.models import Team

bearer_scheme = HTTPBearer(auto_error=False)

# when given authorization credentials in the form of a token, decodes the token to determine the team_id that is currently using the application
def get_current_team(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    if not creds or creds.scheme.lower() != "bearer":
        raise HTTPException(
        status_code=401,
        detail="Missing bearer token"
        )
    token = creds.credentials
    try:
        team_id = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    team = db.query(Team).filter(Team.team_id == team_id).first()
    if not team: 
        raise HTTPException(
            status_code=401,
            detail="Team not found"
        )
    return team
        
