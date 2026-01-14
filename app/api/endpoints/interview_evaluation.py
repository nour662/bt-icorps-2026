from fastapi import APIRouter, Depends, HTTPException
from app.core.db.database import get_db
from app import models
from app.core.config import settings
# from app.worker import evaluate_interviews
from app.schemas.files import PresignRequest, PresignResponse
from app.schemas.interviews import InterviewEvaluationRequest, InterviewEvaluationResponse
from sqlalchemy.orm import Session
from app.models.interviews_table import Interviews
# s3 imports: 
from app.api.endpoints.auth_helper.current_team import get_current_team
from app.storage.s3 import get_s3_client
from uuid import uuid4
import boto3
from botocore.config import Config
    
interview_evaluation_router = APIRouter(
    prefix='/interview', tags=["Interview"]
)

ALLOWED_TYPES = {"application/pdf"}

# Need: 
# route to get an s3 signed url (the frontend will upload the file using that url)
# route to chunk and embed the files (the frontend would send the object key and the backend would retreive the file by the key and then get the text chunking it and embedding it

# route to evaluate the interview (would take a hypothesis as a parameter)
# routes to start interview evaluation (based on a transcript)
@interview_evaluation_router.post("/presign", response_model=PresignResponse)
async def get_presigned_url(req: PresignRequest, team=Depends(get_current_team)):
    if req.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )
    if not req.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only .pdf files allowed"
        )
    
    
    # Using localhost for external presigned URLs
    external_endpoint = settings.S3_ENDPOINT.replace("minio", "localhost")
    
    s3_external = boto3.client(
        "s3",
        endpoint_url=external_endpoint,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name="us-east-1",
        config=Config(signature_version="s3v4"),
    )
    
    key=f"teams/{team.id}/{uuid4()}-{req.filename}"
    url = s3_external.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket" : settings.S3_BUCKET_NAME,
            "Key" : key,
            "ContentType" : "application/pdf"
        },
        ExpiresIn=600 #10 mintues
    )
    
    response = PresignResponse(
        upload_url=url,
        object_key=key
    )
    return response


@interview_evaluation_router.post("/evaluate_interview")
async def evaluate_interview(data = InterviewEvaluationRequest, db : Session = Depends(get_db), team=Depends(get_current_team)):
    # need to first add the interview to the database
    # pass in the hypothesis id and the interview id and team id
    new_interview = Interviews(
        team_id=team.id,
        hypothesis_id=data.hypothesis_id,
        s3_key=data.s3_key,
        evaluated=False
    )
    db.add(new_interview)
    db.commit()
    task = evaluate_interview_task.delay(
        hypothesis_id = hypothesis_addition.id,
        team_id = team.id,
        interview_id = new_interview.id
    )
    return {
        "task_id": task.id,
        "status": "Processing",
        "interviewee_id": new_interview.id,
    }

@interview_evaluation_router.get("/status/{task_id}")
async def get_status(task_id : str):
    result = AsyncResult(task_id)
    return {
        "task_id" : task_id,
        "status" : result.status
    }
@interview_evaluation_router.get("/result/{interview_id}", response_model=InterviewEvaluationResponse)
async def get_result(interview_id :int):
    interview = db.query(Interviews).filter(Interviews.id == interview_id)
    response = InterviewEvaluationResponse(
        evaluation = interview.interviews_output,
        summary = interview.interviews_summar
    )
    return response

    



#@interview_evaluation_router.post("/evaluate_interview")