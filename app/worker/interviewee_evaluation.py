import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.core.celery_app import celery_app

# from langchain_community.document_loaders import PyPDFLoader
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts.chat import ChatPromptTemplate
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
from pgvector.sqlalchemy import Vector
from app.core.config import settings
from app.database.process_input_hypothesis import embed_hypothesis
from sqlalchemy.orm import Session
from app.models.hypotheses_table import Hypotheses

@celery_app.task(name="evaluate_interviewee_profile")

def evaluate_interviewee_profile(hypothesis_id:int, hypothesis:str, hypothesis_type: str, db: Session):
    return {
        "message" : "testing"
    }