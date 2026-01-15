from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.db.database import get_db
from app.models.hypotheses_table import Hypotheses
from app.api.endpoints.auth_helper.current_team import get_current_team
from app.schemas.hypothesis import HypothesisDropdown

router = APIRouter(
    prefix='/dropdown', 
    tags=["Dropdown"]
)

@router.get("/teams/{team_id}/hypotheses")
async def get_hypotheses_for_dropdown(team_id: str, db: Session = Depends(get_db)):
    # We only fetch the ID and the Title/Text to keep the response light
    hypotheses = db.query(Hypotheses).filter(Hypotheses.team_id == team_id).all()
    
    return [
        {"id": h.id, "label": h.hypothesis_text[:50] + "..."} 
        for h in hypotheses
    ]