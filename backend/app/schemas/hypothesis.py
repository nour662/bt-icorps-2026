from pydantic import BaseModel, Field
from enum import Enum

class HypothesisType(str, Enum):
    ECOSYSTEM = "Ecosystem"
    CUSTOMER = "Customer"

class HypothesisEvaluationRequest(BaseModel):
    team_id: str
    hypothesis_type: HypothesisType
    hypothesis: str
    # can add an interview questions parameter here if we chose to have the application evaluate hypothesis and question matching rather 
    # question: would we be better off uploading an interview transcript 
class HypothesisEvaluationResponse(BaseModel):
    hypotheses_output : str
    hypotheses_output_score: int = Field(ge=0, le=100)
    
class HypothesisDropdown(BaseModel):
    hypothesis_id: int
    hypothesis: str
    class Config:
        from_attributes = True