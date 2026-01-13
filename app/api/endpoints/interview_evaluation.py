from fastapi import APIRouter, Depends, HTTPException
from app.core.db.database import get_db
from app import models
from app.worker import evaluate_interviews
from app.schemas.
from sqlalchemy.orm import Session
from app.core.db.database import get_db
from app.models.interviews_table import Interviews
# s3 imports: 
from app.api.endpoints.auth_helper.current_team import get_current_team
# from app.storage.s3 import get_s3_client
import uuid
interview_evaluation_router = APIRouter(
    prefix='/interview', tags=["Interview"]
)


# Need: 
# route to get an s3 signed url (the frontend will upload the file using that url)
# route to chunk and embed the files (the frontend would send the object key and the backend would retreive the file by the key and then get the text chunking it and embedding it

# route to evaluate the interview (would take a hypothesis as a parameter)
# routes to start interview evaluation (based on a transcript)
@interview_evaluation_router.get("/presign")
async def get_presigned_url(team=Depends(get_current_team))
    s3 = get_s3_client()
    key=f"{team.id}/{uuid.uuid4().pdf}"
    url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket" : settings.S3_BUCKET_NAME,
            "Key" : key,
            "ContentType" "application/pdf"
        }
        ExpiresIn=600 #10 mintues
    )
    return {
        "upload_url" : url,
        "object_key" : key
    }

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
    return {
        "message" : "testing"
    }
    



#@interview_evaluation_router.post("/evaluate_interview")