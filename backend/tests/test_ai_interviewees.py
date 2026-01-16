import httpx
import pytest
import time

BASE_URL = "http://localhost:8000"

# Note: This test assumes you've already run the Hypothesis test 
# so you have a valid team_id and hypothesis_id.
@pytest.mark.parametrize("hypothesis_id", [1, 2]) # Replace with IDs from your DB
def test_persona_generation_pipeline(hypothesis_id):
    
    gen_resp = httpx.get(f"{BASE_URL}/interviewee/generate_relevant_personas/{hypothesis_id}")
    
    assert gen_resp.status_code == 200
    task_id = gen_resp.json().get("task_id")
    print(f"✔️ Task Started: {task_id}")

    # --- 2. POLL FOR COMPLETION ---
    finished = False
    for _ in range(60):  # 60 second timeout
        status_resp = httpx.get(f"{BASE_URL}/interviewee/status/{task_id}")
        status = status_resp.json().get("status")
        
        if status == "SUCCESS":
            finished = True
            print("✅ AI has finished generating personas.")
            break
        elif status == "FAILURE":
            pytest.fail("Worker failed to generate personas.")
            
        print("⏳ AI is thinking...")
        time.sleep(2)

    assert finished, "Persona generation timed out."

    # --- 3. FETCH & VERIFY THE RESULTS ---
    results_resp = httpx.get(f"{BASE_URL}/interviewee/relevant_interviewees/{hypothesis_id}")
    assert results_resp.status_code == 200
    
    data = results_resp.json()
    personas = data.get("relevant_customers", [])
    
    print(f"📊 Found {len(personas)} suggested personas:")
    for p in personas:
        print(f"- {p.get('position')} in {p.get('industry')} ({p.get('role')})")

    # Verify we got the "at least 5" personas promised in your prompt
    assert len(personas) >= 5, f"Expected 5+ personas, but got {len(personas)}"