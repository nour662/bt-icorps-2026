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
    is_good_fit : bool
    score: int = Field(ge=0, le=100)
    reasoning : str
    suggested_questions: list[str]
    