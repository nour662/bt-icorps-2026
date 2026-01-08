import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv #dotenv to read from env
from sqlalchemy.orm import Session
from app.models.hypotheses_table import Hypotheses



def save_hypothesis(db: Session, team_id: str, hypothesis_input: str, h_type: str):
    vector = embed_hypothesis(hypothesis_input)

    # creating database object
    new_hypo = Hypotheses(
        team_id = team_id,
        type = h_type,
        hypothesis=hypothesis_input,
        evalulated=False,
        hypotheses_output = None, # none for now
        embedding=vector
    )
    
    try:
        db.add(new_hypo)
        db.commit()
        print(f"Hypothesis {h_type} stored successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

def embed_hypothesis(input_hypothesis):
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

    hypothesis_vector = embeddings_model.embed_query(input_hypothesis) # embed hypothesis inputted by user

    return hypothesis_vector
