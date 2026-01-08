from pydantic import BaseModel, Field
from enum import Enum

class HypothesisType(str, Enum):
    ECOSYSTEM = "Ecosystem"
    CONSUMER = "Consumer"

class HypothesisEvaluationRequest(BaseModel):
    team_id: str
    hypothesis: str
    industry: str | None = None
    hypothesis_type: HypothesisType
    # can add an interview questions parameter here if we chose to have the application evaluate hypothesis and question matching rather 
    # question: would we be better off uploading an interview transcript 
class HypothesisEvaluationResponse(BaseModel):
    hypotheses_output : str
    hypotheses_output_score: int = Field(ge=0, le=100)