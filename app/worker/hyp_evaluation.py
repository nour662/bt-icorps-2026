import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.core.celery_app import celery_app

# from operator import itemgetter
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.output_parsers import StrOutputParser
# from langchain_postgres import PGVector 
from app.core.config import settings
from app.systemprompts.hyp_evaluation_prompt import EVALUATION_PROMPT
from app.database.process_input_hypothesis import embed_hypothesis
from sqlalchemy.orm import Session
from app.core.db.database import SessionLocal
from app.models.hypotheses_table import Hypotheses
from app.models.team_table import Team

#needed for celery task
from app.core.celery_app import celery_app
from app.worker.rag_functions import top_k_chunks, format_rows_for_prompt


# Create the DB connection URL but not sure if the .replace is needed or correct
#Note: if "postgresql://" in connection_url and "psycopg" not in connection_url: connection_url = connection_url.replace("postgresql://", "postgresql+psycopg://")
connection_url = str(settings.DATABASE_URL)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


#celery route for tasks user_persona_rec_task
# --- CELERY TASK ---
#def evaluate_hypothesis_task(user_hypothesis: str):
#    result = rag_chain.invoke(user_hypothesis)
#    return result

@celery_app.task(name="evaluate_hypothesis_task", bind=True)
def evaluate_hypothesis_task(self, hypothesis_id: int, hypothesis_text: str, hypothesis_type: str, team_id: str):    

    
    print(f" Worker check for Hypothesis ID: {hypothesis_id}")
    
    db = SessionLocal()
    embedding = embed_hypothesis(hypothesis_id, hypothesis_text, db)
    results = top_k_chunks(db, embedding, 5 , "Past Data")

    llm = ChatOpenAI(
       model="gpt-4o", 
       api_key=settings.OPENAI_API_KEY,
       base_url=settings.OPENAI_BASE_URL
    )
    guidelines_context = format_rows_for_prompt(results)

    team = db.query(Team).filter(Team.id == team_id).first()


    try:
        prompt_inputs = {
        "guidelines" : guidelines_context,
        "hypothesis" : hypothesis_text,
        "hypothesis_type" : hypothesis_type,
        "team_id" : team_id,
        "industry" : team.industry
        }
        prompt = EVALUATION_PROMPT.format_messages(**prompt_inputs)
        response = llm.invoke(prompt)
        response = response.content
        response_json = json.loads(response)
        score = response_json["score"]
        ai_response = response_json["output"]
        # D. UPDATE DATABASE
        # Fetch the row we created in the API
        record = db.query(Hypotheses).filter(Hypotheses.id == hypothesis_id).first()
        
        if record:
            record.hypotheses_output = ai_response  # Ensure your table has this column!
            print("\n" + record.hypotheses_output + "\n")
            record.hypotheses_output_score = score                # Ensure your table has this column!
            record.evaluated = True        # Critical for Frontend Polling
            db.commit()
            print(f"Success: Updated Hypothesis {hypothesis_id}")
        else:
            print(f"Error: Hypothesis ID {hypothesis_id} not found in DB.")

    except Exception as e:
        print(f"Worker Failed: {e}")
        db.rollback()
        # Update status to FAILED so frontend doesn't hang
        record = db.query(Hypotheses).filter(Hypotheses.id == hypothesis_id).first()
            
    finally:
        # E. CLOSE DB SESSION
        db.close()

    return "Evaluation Task Finished" 
    
