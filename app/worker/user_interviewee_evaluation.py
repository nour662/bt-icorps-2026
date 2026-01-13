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
        guidelines = "none for now" # insert once we figure out logic
        
        prompt = USER_PERSONA_EVALUATION_PROMPT
        
        # idk if this is right :C
        ai_call = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a professional I-Corps consultant."},
                      {"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        evaluation = json.loads(ai_call.choices[0].message.content)

        # update database
        interviewee.customers_output = evaluation.get("analysis")
        interviewee.customers_output_score = evaluation.get("score")
        interviewee.customer_checked = True  # finished checking customer
        
        db.commit()
        print(f"Successfully evaluated {interviewee.customer_name}")

    except Exception as e:
        db.rollback()
        print(f"Worker Failed: {e}")
    finally:
        db.close()
        
        # ai evaluation
    