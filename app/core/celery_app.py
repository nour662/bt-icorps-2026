import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# obtains the Celery broker url from the .env file (if it is not there then defaults to the standard local Redis port for testing purposes)
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# initializing Celery
celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        #"app.tasks.ingestion",
        #"app.tasks.evaluation"
        #"app.tasks.initialize_db",
        #"tasks.testing"
    ]
)

# configuration settings
celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    imports=["app.tasks"]
)