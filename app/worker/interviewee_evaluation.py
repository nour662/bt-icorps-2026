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
from langchain_openai import ChatOpenAI
from app.models.ai_interviewees_table import AI_Interviewees

from app.systemprompts.user_persona_rec_prompt import USER_PERSONA_REC_EVALUATION_PROMPT

@celery_app.task(name="evaluate_interviewee_profile", bind=True)

def evaluate_interviewee_profile(self, hypothesis_id:int):
    db = SessionLocal()
    
    try:
        hypo = db.query(Hypotheses).filter(Hypotheses.id == hypothesis_id).first() # get associated hypothesis
        if not hypo:
            print(f"This hypothesis does not exist")
            return
        
        llm = ChatOpenAI(
            model="gpt-4o", 
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            model_kwargs={"response_format": {"type": "json_object"}}
        )
        
        guidelines = "none for now"
        
        
        prompt_inputs = {
            "guidelines" : guidelines, # add if necessary later
            "hypothesis" : f"{hypo.hypothesis}. Respond with a list of personas in JSON format."
        }
        
        prompt = USER_PERSONA_REC_EVALUATION_PROMPT.format_messages(**prompt_inputs)

        response = llm.invoke(prompt)
        
        # parse json object
        response_json = json.loads(response.content)
        persona_list = response_json.get("personas", [])
        
        # insert into ai interviewees table
        # handle formatting of AI output
        if isinstance(response_json, dict):
            persona_list = response_json.get("personas", [])
        elif isinstance(response_json, list):
            persona_list = response_json
        else:
            persona_list = []
            
        new_records = []
        for p in persona_list:
            clean_p = {str(k).strip(): v for k, v in p.items()}
            
            new_persona = AI_Interviewees(
                hypothesis_id=hypothesis_id,
                company_type=clean_p.get("Company Type"),
                market_segment=clean_p.get("Market Segment"),
                industry=clean_p.get("Industry"),
                position=clean_p.get("Position"),
                role=clean_p.get("Role"),
                outreach_methods=clean_p.get("Recommended Outreach Methods")
            )
            new_records.append(new_persona)
            
        if new_records:
            db.add_all(new_records)
            db.commit()
            print(f"Successfully saved {len(new_records)} generated personas for Hypo {hypothesis_id}")
        
    except Exception as e:
        db.rollback()
        print(f"Worker Error: {str(e)}")
    finally:
        db.close()
    

    
    


    