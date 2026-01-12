from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.document_chunk_table import DocumentChunk
from app.models.hypotheses_table import Hypotheses

# determine optimal number of chunks to find
def get_top_5_relevant_chunks(db: Session, hypothesis_id: int, team_id: str):
    
    hypo_record = db.query(Hypotheses).filter(Hypotheses.id == hypothesis_id).first()
    if not hypo_record or hypo_record.hypothesis_embedding is None:
        raise ValueError("Hypothesis embedding not found in database.")
    
    hypo_vector = hypo_record.hypothesis_embedding
   
    # find top 5 relevant number of chunks for now
    top_5 = (
        select(DocumentChunk)
        .filter(DocumentChunk.team_id == team_id)
        # use semantic search to find data that is most similar in meaning
        .order_by(DocumentChunk.embedding.cosine_distance(hypo_vector)) 
        .limit(5)
    )
    
    results = db.execute(top_5).scalars().all()
    
    return [chunk.content for chunk in results] # return list of strings for LLM to process
