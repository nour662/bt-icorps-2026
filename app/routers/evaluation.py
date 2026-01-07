from fastapi import APIRouter
from pydantic import BaseModel

evaluation_router = APIRouter(
    # prefix='/evaluate_hypothesis', tags=["Evaluation"]
)
class HypothesisRequest(BaseModel):
    team_id: 
    hypothesis: str
    industry: str | None = None
    # can add an interview questions parameter here if we chose to have the application evaluate hypothesis and question matching rather 
    # question: would we be better off uploading an interview transcript 

@evaluation_router.post("/evaluate")
async def evaluate_hypothesis(data: HypothesisRequest):
    # pass to celery