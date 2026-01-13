from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.db.database import engine, get_db
from app.storage.s3 import ensure_bucket_exists

# importing routes
from app.api.endpoints.teams import teams_router as teams_router
from app.api.endpoints.hypothesis_evaluation import evaluation_router as hypothesis_router 
from app.api.endpoints.interviewee_profile import interviewee_router as interviewee_router 



# from app.storage.init import ensure_bucket_exists
import redis
import os

app = FastAPI(title="Interview Info App API")

# defining all routes in main
app.include_router(teams_router)
app.include_router(hypothesis_router)
app.include_router(interviewee_router)

with engine.connect() as conn:
    # if the database does not already have the capability, adds the app that allows for vector computation abilities
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()

# Base.metadata.create_all(bind=engine)

# checks to make sure the s3 bucket for interview data storage exist and was not deleted somehow
# this can be removed once we switch to AWS in prod
@app.on_event("startup")
def startup():
    ensure_bucket_exists()

# these are a couple of basic routes used to test the API and make sure that the database is connected properly
@app.get("/")
def read_root():
    return{
        "status":"online",
        "message" : "Welcome to the Interview Info App API"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    # testing the database connection
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
    
    # testig the redis connection (for celery):
    try:
        r = redis.from_url(os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"))
        r.ping()
        redis_status = "connected"
    except Exception as e:
        redis_status = f"disconnected: {str(e)}"
    return {
        "database" : db_status,
        "redis" : redis_status,
        "environment": "development"
    }
