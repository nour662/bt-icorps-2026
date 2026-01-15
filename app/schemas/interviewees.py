from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import List, Optional

class ExperienceLevel(str, Enum):
    JUNIOR = "Junior"
    MID = "Mid-Level"
    SENIOR = "Senior"
    EXECUTIVE = "Executive"

# real interviewee schemas:

# 1. The base data for an interviewee (The "Persona")
class IntervieweeBase(BaseModel):
    team_id : str
    industry: str
    occupation: str
    experience_level: ExperienceLevel

# 2. Used for the POST /check_persona request
class IntervieweeEvaluationBase(IntervieweeBase):
    #team_id: str
    hypothesis_id: int
    name: str
    interviewee_bio: str

# 3. Used for the GET /results/{id} response
# This matches your Interviewees table columns exactly
class IntervieweeEvaluationResponse(IntervieweeBase):
    id: int
    customer_name: str          # Matches DB
    customer_checked: bool
    customers_output: Optional[str] = None
    customers_output_score: Optional[int] = None

    class Config:
        from_attributes = True # This is still required to read DB objects

# 4. Used for the GET /relevant_customers response
class RelevantIntervieweesList(BaseModel):
    relevant_customers: List[IntervieweeBase]
    
# ai generated schemas:
class GeneratedPersona(BaseModel):

    company_type: str = Field(alias="Company Type")
    market_segment: str = Field(alias="Market Segment")
    industry: str = Field(alias="Industry")
    position: str = Field(alias="Position")
    role: str = Field(alias="Role")
    outreach_methods: str = Field(alias="Recommended Outreach Methods")

    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

class RelevantIntervieweesList(BaseModel):
    relevant_customers: List[GeneratedPersona]