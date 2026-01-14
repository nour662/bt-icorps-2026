from sqlalchemy import text
from sqlalchemy.orm import Session
def top_k_chunks(db: Session, query_embedding, k, search_type, team_id):
    target_table = "past_data" if search_type == "Past Data" else "interviews"
    
    query = text(f"""
        SELECT id, content
        FROM document_chunks
        WHERE team_id = :team_id
        AND s3_key IN (
            SELECT s3_key 
            FROM {target_table} 
            WHERE team_id = :team_id
        )
        ORDER BY embedding <=> :q_emb
        LIMIT :k
    """)

    params = {
        "team_id": team_id,
        "q_emb": str(query_embedding).replace(' ', ''),
        "k": k
    }
    
    # sql = """
    #     SELECT id, content
    #     FROM document_chunks
    #     {where_clause}
    #     ORDER BY embedding <=> :q_emb
    #     LIMIT :k
    # """
    # where_clause = ""
    # params = {
    #     "q_emb": query_embedding,
    #     "k" : k
    # }
    # if (search_type=="Past Data"):
    #     where_clause = "WHERE past_data_id IS NOT NULL"
    # else:
    #     where_clause = "WHERE interview_id IS NOT NULL"
    # rows = db.execute(text(sql.format(where_clause=where_clause)), params).fetchall()
    rows = db.execute(query, params).fetchall()
    return rows

def format_rows_for_prompt(rows):
    if not rows: 
        return "No relevant prior data found"
    return "\n\n".join(
        r.content for r in rows
    )
    