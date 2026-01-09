import sys
from pathlib import Path
from sqlalchemy import inspect, text

# 1. Setup paths to find your app
root = Path(__file__).resolve().parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from app.core.database import engine, Base
# IMPORTANT: Import ALL your models here so the script knows they exist
from app.models.team_table import Team
from app.models.customer_table import Customers
from app.models.hypotheses_table import Hypotheses
from app.models.interviews_table import Interviews
from app.models.document_chunk_table import DocumentChunk

def test_entire_schema():
    print("Starting Full Database Audit...\n")
    inspector = inspect(engine)
    db_tables = inspector.get_table_names()
    
    # Track results
    missing_tables = []
    issues_found = 0

    # 2. Check every model registered in SQLAlchemy's Base
    for table_name, table_obj in Base.metadata.tables.items():
        print(f"--- Checking Table: [{table_name}] ---")
        
        if table_name not in db_tables:
            print(f"MISSING: Table '{table_name}' does not exist in the database.")
            missing_tables.append(table_name)
            issues_found += 1
            continue
        
        # 3. Check individual columns for this table
        db_columns = {c['name']: c for c in inspector.get_columns(table_name)}
        model_columns = table_obj.columns
        
        for col in model_columns:
            if col.name not in db_columns:
                print(f"  ❌ MISSING COLUMN: '{col.name}' is in code but not in DB.")
                issues_found += 1
            else:
                print(f"  ✅ '{col.name}' is present.")

    print("\n" + "="*30)
    if issues_found == 0:
        print("✨ ALL CLEAR: Your database schema matches your Python models perfectly.")
    else:
        print(f"⚠️  FINISHED: Found {issues_found} issues that need fixing.")
        if missing_tables:
            print(f"Tip: Run your 'create_tables' script to add: {missing_tables}")
    print("="*30)

if __name__ == "__main__":
    test_entire_schema()