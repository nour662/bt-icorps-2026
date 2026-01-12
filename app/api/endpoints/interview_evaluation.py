from fastapi import APIRouter, Depends, HTTPException
from app.core.db.database import get_db
from app import models
from app.tasks import evaluate_interviews
from app.schemas.

from sqlalchemy.orm import Session
from app.core.db.database import get_db
from app.models.interviews_table import Interviews

interview_evaluation_router = APIRouter(
    prefix='/interview', tags=["Interview"]
)


# Need: 
# route to get an s3 signed url (the frontend will upload the file using that url)
# route to chunk and embed the files (the frontend would send the object key and the backend would retreive the file by the key and then get the text chunking it and embedding it

# route to evaluate the interview (would take a hypothesis as a parameter)
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

@interview_evaluation_router.post("/process_document")
async def process_document(team_id: str, interviewee_name: str, s3_key: str, db: Session = Depends(get_db)):
    # 1. Create the Interview Record
    new_interview = Interviews(
        team_id=team_id,
        interviewee_name=interviewee_name,
        s3_key=s3_key,
        evaluated=False
    )
    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)
    



@interview_evaluation_router.post("/evaluate_interview")