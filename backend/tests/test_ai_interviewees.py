import httpx
import pytest
import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Import your models and settings
from app.core.db.database import get_db
from app.models.hypotheses_table import Hypotheses
from app.core.config import settings

BASE_URL = "http://localhost:8000"

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# query db to get first associated hyp for each team
@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        
def test_persona_generation_pipeline(db):
    hypo = db.query(Hypotheses).first()
    
    if not hypo:
        pytest.skip("No hypotheses found in database. Run the hypothesis creation test first.")
    
    hypothesis_id = hypo.id
    print(f"Testing Persona Generation for Hypothesis ID: {hypothesis_id}")

    # start generation
    gen_resp = httpx.get(f"{BASE_URL}/interviewee/generate_relevant_personas/{hypothesis_id}")
    
    assert gen_resp.status_code == 200
    task_id = gen_resp.json().get("task_id")
    print(f"✔️ Task Started: {task_id}")

    # poll for completion
    finished = False
    for _ in range(60):  # 120 second timeout total
        status_resp = httpx.get(f"{BASE_URL}/interviewee/status/{task_id}")
        status = status_resp.json().get("status")
        
        if status == "SUCCESS":
            finished = True
            print("✅ AI has finished generating personas.")
            break
        elif status == "FAILURE":
            pytest.fail("Worker failed to generate personas.")
            
        time.sleep(2)

    assert finished, "Persona generation timed out."

    # fetch + verify results
    results_resp = httpx.get(f"{BASE_URL}/interviewee/relevant_interviewees/{hypothesis_id}")
    assert results_resp.status_code == 200
    
    data = results_resp.json()
    personas = data.get("relevant_customers", [])
    
    print(f"📊 Found {len(personas)} suggested personas:")
    for p in personas:
        industry = p.get('Industry') or p.get('industry')
        pos = p.get('Position') or p.get('position')
        role = p.get('Role') or p.get('role')
        
        print(f"- {pos} in {industry} ({role})")

    assert len(personas) >= 5, f"Expected 5+ personas, but got {len(personas)}"