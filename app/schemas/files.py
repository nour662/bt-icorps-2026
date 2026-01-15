from pydantic import BaseModel, Field
from enum import Enum

class PresignRequest(BaseModel):
    filename : str = Field(min_length=1, examples=["interview.pdf"])
    content_type : str = Field(mi_length=1, examples=["application/pdf"])
class PresignResponse(BaseModel):
    upload_url : str 
    object_key : str