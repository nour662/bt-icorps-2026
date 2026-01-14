from celery import Celery
from app.core.config import settings


# obtains the Celery broker url from the .env file (if it is not there then defaults to the standard local Redis port for testing purposes)
CELERY_BROKER_URL = settings.CELERY_BROKER_URL
CELERY_RESULT_BACKEND = settings.CELERY_RESULT_BACKEND

# initializing Celery
celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        "app.worker.hyp_evaluation",
        "app.worker.user_interviewee_evaluation",
        "app.worker.interviewee_evaluation"
    ]
)

# configuration settings
celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    # imports=["app.tasks"]  # Commented out to prevent importing PGVector dependencies during migrations
)