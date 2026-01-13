from sqlalchemy import text
from sqlalchemy.orm import Session
def top_k_chunks(db: Session, query_embedding, k, search_type):
    sql = """
        SELECT id, content
        FROM document_chunks
        {where_clause}
        ORDER BY embedding <=> :q_emb
        LIMIT :k
    """
    where_clause = ""
    params = {
        "q_emb": query_embedding,
        "k" : k
    }
    if (search_type=="Past Data"):
        where_clause = "WHERE past_data_id IS NOT NULL"
    else:
        where_clause = "WHERE interview_id IS NOT NULL"
    rows = db.execute(text(sql.format(where_clause=where_clause)), params).fetchall()
    return rows

def format_rows_for_prompt(rows):
    if not rows: 
        return "No relevant prior data found"
    return "\n\n".join(
        r.content for r in rows
    )
    