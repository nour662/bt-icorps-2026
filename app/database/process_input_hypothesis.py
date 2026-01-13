import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv #dotenv to read from env
from sqlalchemy.orm import Session
from app.models.hypotheses_table import Hypotheses
from app.core.db.database import SessionLocal
import tiktoken

MAX_HYPOTHESIS_TOKENS = 3000 # set max value -> can change later

def save_hypothesis(db: Session, team_id: str, hypothesis_input: str, h_type: str):
    # vector = embed_hypothesis(hypothesis_input)

    # creating database object
    new_hypo = Hypotheses(
        team_id = team_id,
        type = h_type,
        hypothesis=hypothesis_input,
        evalulated=False,
        hypotheses_output = None, # none for now
        embedding=None # empty for now
    )
    
    try:
        db.add(new_hypo)
        db.commit()
        print(f"Hypothesis {h_type} stored successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

def embed_hypothesis(hypothesis_id:int, hypothesis_text:str, db: Session):
    # check token size! OR request limit
    token_count = get_tokens(hypothesis_text)
    if token_count > MAX_HYPOTHESIS_TOKENS:
        print(f"Hypothesis is too long")
        return False

    # db = SessionLocal()
    
    try: 
        # get both customer/ecosystem hypothesis
        embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

        vector = embeddings_model.embed_query(hypothesis_text) # embed hypothesis inputted by user
    
        # add into table
            # set embeddings here!
            # only analyze based on value of evaluated
        hypo = db.query(Hypotheses).filter(Hypotheses.id == hypothesis_id).first()
    
        if hypo:
            hypo.embedding = vector
            db.commit()
    except Exception as e:
        db.rollback()
    finally: 
        db.close()


def get_tokens(text: str, model="text-embedding-3-small"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))