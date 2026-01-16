import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.core.celery_app import celery_app

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from app.systemprompts.hyp_evaluation_prompt import EVALUATION_PROMPT
from app.database.process_input_hypothesis import embed_hypothesis
from sqlalchemy.orm import Session
from app.core.db.database import SessionLocal
from app.models.hypotheses_table import Hypotheses
from app.models.team_table import Team
from sqlalchemy import desc, func

#needed for celery task
from app.core.celery_app import celery_app
from app.worker.rag_functions import top_k_chunks_past_data, format_rows_for_prompt

# This embedds the celery task that contains inputs such as the 
# hypothesis text, team id, and hypothesis type


# This embedds the celery task that contains inputs such as the 
# hypothesis text, team id, and hypothesis type


@celery_app.task(name="evaluate_hypothesis_task", bind=True)
def evaluate_hypothesis_task(self, hypothesis_id: int, hypothesis_text: str, hypothesis_type: str, team_id: str):    

    
    print(f" Worker check for Hypothesis ID: {hypothesis_id}")
    
    db = SessionLocal()
    embedding = embed_hypothesis(hypothesis_id, hypothesis_text, db)
    
    # evaluate customer hypothesis against current ecosystem
    if hypothesis_type.lower() == "customer":
        print(f"Running Customer Validation for ID: {hypothesis_id}")
        ecosystem_matches = db.query(
            Hypotheses, 
            (1 - Hypotheses.embedding.cosine_distance(embedding)).label("similarity")
        ).filter(
            Hypotheses.team_id == team_id,
            func.lower(Hypotheses.hyp_type) == "ecosystem"
        ).order_by(desc("similarity")).limit(3).all()
            
        SIMILARITY_THRESHOLD = 0.7
        print(f"The similarity is: {round(ecosystem_matches[0].similarity, 2)} \n")
        if not ecosystem_matches or ecosystem_matches[0].similarity < SIMILARITY_THRESHOLD:
            record = db.query(Hypotheses).filter(Hypotheses.id == hypothesis_id).first()
            record.hypotheses_output = "No Match Found: This customer hypothesis does not align with your current ecosystem."
            record.hypotheses_output_score = 0
            record.evaluated = True
            
            db.commit()
            return "No Ecosystem Matches"
        ecosystem_context = "\n".join([
            f"- {m.Hypotheses.hypothesis} (Similarity: {round(m.similarity, 2)})" 
            for m in ecosystem_matches
        ])
        print(f"\n--- ECOSYSTEM CONTEXT PREPARED ---\n{ecosystem_context}\n----------------------------------")
    else:
        print(f"Running Ecosystem Evaluation for ID: {hypothesis_id}")
        
    results = top_k_chunks_past_data(db, embedding, 5)

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

    return "Hypothesis Evaluation Task Finished" 
    
