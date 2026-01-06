from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import engine, Base, get_db
import redis
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Interview Info App API")

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