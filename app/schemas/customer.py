from pydantic import BaseModel, Field
from enum import Enum

class ExperienceLevel(str, Enum):
    JUNIOR = "Junior"
    MID = "Mid-Level"
    SENIOR = "Senior"
    EXECUTIVE = "Executive"
class CustomerEvaluationBase(BaseModel):
    team_id: str
    hypothesis: str
    name : str
    industry : str
    occupation : str
    experience_level : ExperienceLevel
class CustomerEvaluationResponse(BaseModel):
    customers_output : str
    customers_output_score: int = Field(ge=0, le=100)
    