import sys
import os
import json

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
from app.core.db.database import SessionLocal

@celery_app.task(name="evaluate_interviewee_profile", bind=True)

def evaluate_interviewee_profile(self, hypothesis_id:int, hypothesis:str, hypothesis_type: str):
    db = SessionLocal()
    
    ai_response = """
        [
            {
                "name" : "something",
                "indsutry" : "something",
            },
            {
                "name2" : "something2",
                "indsutry2" : "something2",
            },
        ]
    """ 
    data = json.loads(ai_response)
    for i in range (0, len(data)):
        addition = Hypotheses(
            hypothesis_id = hypothesis_id,
            company_type = data[i]["Company Type"],
            market_segment = data[i]["Market Segment"],
            industry = data[i]["Industry"],
            position = data[i]["Position"],
            role = data[i]["Role"],
            outreach_methods = data[i]["Recommended Outreach Methods"]
        )
        db.add(addition)
    db.commit()
    return
    
    
    # need to pass in the hypothesis text here
    prompt=""
    
    


    