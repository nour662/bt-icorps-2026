from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

class ExperienceLevel(str, Enum):
    JUNIOR = "Junior"
    MID = "Mid-Level"
    SENIOR = "Senior"
    EXECUTIVE = "Executive"

# 1. The base data for an interviewee (The "Persona")
class IntervieweeBase(BaseModel):
    team_id : str
    industry: str
    occupation: str
    experience_level: ExperienceLevel

# 2. Used for the POST /check_persona request
class IntervieweeEvaluationBase(IntervieweeBase):
    team_id: str
    hypothesis_id: int
    name: str

# 3. Used for the GET /results/{id} response
# This matches your Interviewees table columns exactly
class IntervieweeEvaluationResponse(IntervieweeBase):
    id: int
    team_id: str
    customer_name: str
    customer_checked: bool
    customers_output: Optional[str] = None
    customers_output_score: Optional[int] = Field(None, ge=0, le=100)

    class Config:
        from_attributes = True # Allows SQLAlchemy objects to be converted to Pydantic

# 4. Used for the GET /relevant_customers response
class RelevantIntervieweesList(BaseModel):
    relevant_customers: List[IntervieweeBase]