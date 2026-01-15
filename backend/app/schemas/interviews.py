from pydantic import BaseModel

class InterviewEvaluationRequest(BaseModel):
    hypothesis_id : int
    s3_key : str

class InterviewEvaluationResponse(BaseModel):
    evaluation : str
    summary : str