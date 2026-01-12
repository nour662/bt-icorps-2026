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


@celery_app.task(name="evaluate_hypothesis_task")

def evaluate_hypothesis_task(hypothesis_id:int, hypothesis:str, hypothesis_type: str):
    db = SessionLocal()
    # if ecosystem, evaluate with PGVector
    hypothesis_embedding = embed_hypothesis(hypothesis_hypothesis)
    # if (hypothesis_type == "Customer"):
     # RAG logic here - make sure to sort by ecosystem
    # make OpenAI call - can define a request body baseed on the type r can make two separate calls

    # store results in the output and score section of the hypothesis table
    # return
    return {
        "message" : "done"
    }
    
