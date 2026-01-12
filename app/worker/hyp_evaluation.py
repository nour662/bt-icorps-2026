import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.core.celery_app import celery_app

from operator import itemgetter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.output_parsers import StrOutputParser
from langchain_postgres import PGVector 
from app.core.config import settings
from app.systemprompts.hyp_evaluation_prompt import EVALUATION_PROMPT
from app.core.config import settings
from app.database.process_input_hypothesis import embed_hypothesis
from sqlalchemy.orm import Session
from app.models.hypotheses_table import Hypotheses

#needed for celery task
from app.core.celery_app import celery_app
from app.core.db.database import SessionLocal  # <--- Check what this path is and if we have it 
from sqlalchemy.orm import Session

# 1. The reason why we are embedding is because yes we are receving the vectors from the DB
# But when you receive vectors they are just numbers. We need to embed the vectors inorder for 
# the LLM to understand them and use them for searching and matching.
embeddings = OpenAIEmbeddings(
    api_key=settings.OPENAI_API_KEY, 
    model="text-embedding-3-small"
)

# Create the DB connection URL but not sure if the .replace is needed or correct
#Note: if "postgresql://" in connection_url and "psycopg" not in connection_url: connection_url = connection_url.replace("postgresql://", "postgresql+psycopg://")
connection_url = str(settings.DATABASE_URL)

# 2. Connect to the "hypothesis_rules" DB collection
vector_store = PGVector(
    embeddings=embeddings,
    collection_name="hypothesis_rules", #Match the name of the table in the DB
    connection=connection_url,
    use_jsonb=True,
)

# 3. Create the Search Engine
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 4. Define the Chain
# Input expected: { "hypothesis": "...", "team_id": "...", "type": "..." }
rag_chain = (
    {
        # SEARCH STEP: Take the hypothesis text, find matching rules in DB
        "guidelines": itemgetter("hypothesis") | retriever | format_docs,
        
        # PASSTHROUGH: Pass the raw data to the prompt
        "hypothesis": itemgetter("hypothesis"),
        "team_id": itemgetter("team_id"),
        "hypothesis_type": itemgetter("hypothesis_type")
    }
    | EVALUATION_PROMPT
    | ChatOpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY)
    | StrOutputParser()
)


#celery route for tasks user_persona_rec_task
# --- CELERY TASK ---
#def evaluate_hypothesis_task(user_hypothesis: str):
#    result = rag_chain.invoke(user_hypothesis)
#    return result

@celery_app.task(name="evaluate_hypothesis_task", bind=True)
def evaluate_hypothesis_task(self, hypothesis_id: int, hypothesis_text: str, hypothesis_type: str, team_id: str):
    
    #1. Opens a DB session.
    #2. Runs the RAG chain.
    #3. Saves result to Postgres.
    
    print(f" Worker check for Hypothesis ID: {hypothesis_id}")
    
    # A. OPEN DB SESSION (Manually) need to change variable names to whatever is in the db
    db = SessionLocal()
    
    try:
        # B. RUN RAG CHAIN
        # We pass the arguments directly into the chain
        rag_input = {
            "hypothesis": hypothesis_text,
            "team_id": team_id,
            "hypothesis_type": hypothesis_type
        }
        
        # This performs the Vector Search + OpenAI Generation
        ai_response = rag_chain.invoke(rag_input)
        print("\n" + ai_response + "\n")
        print(type(ai_response))
        # C. PARSE SCORE (Basic Logic)
        score = 0
        if "Score:" in ai_response:
            try:
                # Extracts the number after "Score:"
                score_part = ai_response.split("Score:")[1].split("/")[0].strip()
                score = int(score_part)
            except ValueError:
                score = 0 # Default if parsing fails

        # D. UPDATE DATABASE
        # Fetch the row we created in the API

        #FIND THESE ROW NAMES AND MAKE SURE THEY MATCH THE DB
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

        #Find THESE ROW NAMES AND MAKE SURE THEY MATCH THE DB
        record = db.query(Hypotheses).filter(Hypotheses.id == hypothesis_id).first()
        # if record:
        #     record.status = "FAILED"
        #     db.commit()
            
    finally:
        # E. CLOSE DB SESSION
        db.close()

    return "Evaluation Task Finished" 
    
