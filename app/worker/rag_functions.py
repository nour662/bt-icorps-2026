from sqlalchemy import text
from sqlalchemy.orm import Session
def top_k_chunks_past_data(db: Session, query_embedding, k):
    sql = """
        SELECT id, content
        FROM document_chunks
        WHERE past_data_id IS NOT NULL
        ORDER BY embedding <=> :q_emb
        LIMIT :k
    """
    params = {
        "q_emb": query_embedding,
        "k" : k
    }
    rows = db.execute(text(sql), params).fetchall()
    return rows

def top_k_chunks_interview_data(db: Session, query_embedding, k, interview_id):
    sql = """
        SELECT id, content
        FROM document_chunks
        WHERE interview_id = :interview_id
        ORDER BY embedding <=> :q_emb
        LIMIT :k
    """
    params = {
        "interview_id" : interview_id,
        "q_emb": query_embedding,
        "k" : k
    }
    rows = db.execute(
        text(sql), 
        params
    ).fetchall()
    return rows

def format_rows_for_prompt(rows):
    if not rows: 
        return "No relevant prior data found"
    return "\n\n".join(
        r.content for r in rows
    )
    