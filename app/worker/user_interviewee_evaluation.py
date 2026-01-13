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

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

@celery_app.task(name="evaluate_interviewee_task", bind=True)
def evaluate_interviewee_task(self, interviewee_id: int):
    db = SessionLocal()
    
    try:
        interviewee = db.query(Interviewees).filter(Interviewees.id == interviewee_id).first() # get info from database
        if not interviewee:
            print(f"This person does not exist")
            return
        # insert searching past database here
        
        # ai evaluation 
        guidelines = "none for now" # insert once we figure out logic
        
        prompt = f"""
        
        Evaluation Guidelines:
        {guidelines}

        Interviewee Profile:
        Name: {interviewee.customer_name}
        Occupation: {interviewee.customer_occupation}
        Industry: {interviewee.customer_industry}
        Experience/Input: {interviewee.customer_experience}

        Task: Analyze if this interview provides high-quality data for an I-Corps hypothesis.
        Return ONLY a JSON object:
        {{
            "analysis": "A 2-3 sentence summary of the validation or insights gained.",
            "score": 0-5 (Integer: How valuable/relevant was this interview?)
        }}
        """
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
    