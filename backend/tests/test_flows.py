import httpx
import pytest
import pandas as pd
import numpy as np
import time

BASE_URL = "http://localhost:8000"

def load_csv():
    df = pd.read_csv("/code/src/test_file/test_data.csv")
    # FIX 1: Replace NaN with None so they become 'null' in JSON instead of crashing
    df = df.replace({np.nan: None})
    return df.to_dict(orient="records")

@pytest.mark.parametrize("row", load_csv())
def test_full_pipeline(row):
    # FIX 2: Define t_id immediately
    t_id = str(row["team_ID"])
    
    # --- 1. SIGNUP ---
    signup_data = {
        "team_id": t_id,
        "team_name": row["team_name"],
        "industry": row["industry"],
        "password": str(row["password"])
    }
    httpx.post(f"{BASE_URL}/teams/create_account", json=signup_data)

    # --- 2. LOGIN ---
    login_data = {
        "team_id": t_id,
        "password": str(row["password"])
    }
    login_resp = httpx.post(f"{BASE_URL}/teams/sign_in", json=login_data)
    assert login_resp.status_code == 200
    token = login_resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # --- 3. DUAL HYPOTHESIS SUBMISSION ---
    # We check both columns and only send if they aren't None (null)

    if row.get("ecosystem_hypothesis"):
        hyp_payload = {
            "team_id": t_id,
            "hypothesis_type": "Ecosystem",
            "hypothesis": row["ecosystem_hypothesis"]
        }
        resp = httpx.post(f"{BASE_URL}/hypothesis/evaluate", json=hyp_payload, headers=headers)
        assert resp.status_code == 200
        
        task_id = resp.json().get("task_id")
        hyp_id = resp.json().get("hypothesis_id")
        
        while True:
            status_resp = httpx.get(f"{BASE_URL}/hypothesis/status/{task_id}")
            if status_resp.json().get("status") == "SUCCESS":
                break
            time.sleep(1) # Wait for AI to finish
            
        result_resp = httpx.get(f"{BASE_URL}/hypothesis/results/{hyp_id}", headers=headers)
        final_data = result_resp.json()
        
        print("\n--- ECOSYSTEM HYPOTHESIS EVALUATION ---")
        print("Evaluation:", final_data.get("hypotheses_output"))
        print("Score:", final_data.get("hypotheses_output_score"))

        
    if row.get("customer_hypothesis"):
        hyp_payload = {
            "team_id": t_id,
            "hypothesis_type": "Customer",
            "hypothesis": row["customer_hypothesis"]
        }
        assert resp.status_code == 200
        
        task_id = resp.json().get("task_id")
        hyp_id = resp.json().get("hypothesis_id")
        
        while True:
            status_resp = httpx.get(f"{BASE_URL}/hypothesis/status/{task_id}")
            if status_resp.json().get("status") == "SUCCESS":
                break
            time.sleep(1) # Wait for AI to finish
            
        result_resp = httpx.get(f"{BASE_URL}/hypothesis/results/{hyp_id}", headers=headers)
        final_data = result_resp.json()
        
        print("\n--- CUSTOMER HYPOTHESIS EVALUATION ---")
        print("Evaluation:", final_data.get("hypotheses_output"))
        print("Score:", final_data.get("hypotheses_output_score"))
