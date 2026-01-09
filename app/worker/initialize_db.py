import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.core.celery_app import celery_app
from sqlalchemy import text, inspect
from app.core.database import engine, Base

# Import models so Base can see them for create_all
from app.models.team_table import Team
from app.models.customers_table import Customers
from app.models.hypotheses_table import Hypotheses
from app.models.interviews_table import Interviews
from app.models.document_chunk_table import DocumentChunk

@celery_app.task(name="tasks.init_db")
def init_db_task():
    """
    Celery task to initialize the database. 
    Running this inside a worker container resolves 'db' automatically.
    """
    results = {"status": "started", "logs": []}
    
    try:
        # 1. Test Connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            results["logs"].append("Connection to 'db' successful!")

        # 2. Create Tables
        Base.metadata.create_all(bind=engine)
        results["logs"].append("Tables created/verified.")
        results["status"] = "success"
        
    except Exception as e:
        results["status"] = "error"
        results["logs"].append(f"Error: {str(e)}")
        
    check_tables()
    
    return results

def check_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("--- Database Audit ---")
    if not tables:
        print("❌ No tables found. Did you run create_all()?")
    else:
        print(f"✅ Found {len(tables)} tables:")
        for table in tables:
            print(f" - {table}")
            # Optional: Check columns for a specific table
            columns = [c['name'] for c in inspector.get_columns(table)]
            print(f"   Columns: {columns}")

# main for testing
if __name__ == "__main__":
    print("Sending initialization task to Celery Worker...")
    
    # 1. Trigger the task and save the AsyncResult object
    task_result = init_db_task.delay()
    
    print(f"Waiting for worker (Service: worker) to finish task {task_result.id}...")
    
    # 2. Call .get() on the task_result
    try:
        final_output = task_result.get(timeout=15)
        print(f"\nStatus: {final_output.get('status')}")
        for log in final_output.get('logs', []):
            print(f"   - {log}")
    except Exception as e:
        print(f"Task failed or timed out: {e}")