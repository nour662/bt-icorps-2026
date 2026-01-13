import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import openai
from app.core.celery_app import celery_app
from app.core.db.database import SessionLocal
from app.models.interviewees_table import Interviewees
from app.models.hypotheses_table import Hypotheses
from sqlalchemy import text
from app.core.config import settings
from app.systemprompts.user_persona_evaluation_prompt import USER_PERSONA_EVALUATION_PROMPT
from langchain_openai import ChatOpenAI

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

@celery_app.task(name="evaluate_interviewee_task", bind=True)
def evaluate_interviewee_task(self, interviewee_id: int, hypothesis_text: str):
    db = SessionLocal()
    
    try:
        interviewee = db.query(Interviewees).filter(Interviewees.id == interviewee_id).first() # get info from database
        if not interviewee:
            print(f"This person does not exist")
            return
        # insert searching past database here??
        # ai evaluation 
        llm = ChatOpenAI(
            model="gpt-4o", 
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            model_kwargs={"response_format": {"type": "json_object"}}
        )
        
        guidelines = "none for now" # insert once we figure out logic
        
        prompt_inputs = {
        "guidelines" : guidelines, # add if necessary later
        "hypothesis" : hypothesis_text,
        "name": interviewee.customer_name,      
        "industry": interviewee.customer_industry,
        "occupation": interviewee.customer_occupation,
        "experience": interviewee.customer_experience
        }
        prompt = USER_PERSONA_EVALUATION_PROMPT.format_messages(**prompt_inputs)
        response = llm.invoke(prompt)
        print(f"DEBUG - RAW AI RESPONSE: {response.content}")
        response_content = response.content
        if "```json" in response_content:
            response_content = response_content.split("```json")[1].split("```")[0].strip()
            
        response_json = json.loads(response_content)

        # update database
        interviewee.customers_output = response_json.get("output") # Based on your logic
        interviewee.customers_output_score = response_json.get("score")
        interviewee.customer_checked = True
        
        db.commit()
        print(f"Successfully evaluated {interviewee.customer_name}")

    except Exception as e:
        db.rollback()
        print(f"Worker Failed: {e}")
    finally:
        db.close()
        
        # ai evaluation
    