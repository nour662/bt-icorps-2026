import sys
from pathlib import Path
from sqlalchemy import text

# Setup paths
root = Path(__file__).resolve().parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
    
from app.core.db.database import engine
from app.core.db.base import Base
# Ensure models are imported so Base knows about them
from app.models.document_chunk_table import DocumentChunk 

def create_tables():
    print(f"Connecting to: {engine.url}")
    try:
        # 1. Test Connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("Connection successful!")

        # 2. Create Tables
        Base.metadata.create_all(bind=engine)
        print("SQLAlchemy 'create_all' command sent.")
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    create_tables()