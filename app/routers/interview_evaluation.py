from fastapi import APIRouter
from pydantic import BaseModel
from app.core.database import get_db
from app import models
from app.tasks import evaluate_interviews
from app.schemas.

interview_evaluation_router = APIRouter(
    prefix='/interview', tags=["Interview"]
)


# Need: 

# routes to start interview evaluation (based on a transcript)
@interview_evaluation_router.post("/upload_transcript")
async def upload_file(file: UploadFile = File()):
    # checking if the file is a parsable format
    allowed_types = ["text/plain", "application/pdf"]
    if (file.content_type not in allowed_types):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type"
        )
    




@interview_evaluation_router.post("/evaluate_interview")