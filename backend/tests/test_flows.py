import httpx
import pytest
import pandas as pd
import numpy as np
import time

BASE_URL = "http://localhost:8000"
REPORT_FILE = "evaluation_report.txt"

def load_csv():
    df = pd.read_csv("/code/src/test_file/test_data.csv")
    df = df.replace({np.nan: None})
    return df.to_dict(orient="records")

@pytest.fixture(scope="session", autouse=True)
def create_report_header():
    with open(REPORT_FILE, "w") as f:
        f.write("=== DEPENDENCY-BASED RESEARCH REPORT ===\n")
        f.write(f"Run Date: {time.ctime()}\n")
        f.write("Logic: Ecosystem MUST succeed before Customer is triggered.\n")
        f.write("="*50 + "\n\n")

@pytest.mark.parametrize("row", load_csv())
def test_sequential_dependency_pipeline(row):
    t_id = str(row["team_ID"])
    
    # 1. AUTHENTICATION
    login_resp = httpx.post(f"{BASE_URL}/teams/sign_in", json={"team_id": t_id, "password": str(row["password"])})
    token = login_resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    with open(REPORT_FILE, "a") as f:
        f.write(f"TEAM: {row['team_name']} ({t_id})\n")
        
        # --- STEP A: ECOSYSTEM HYPOTHESIS ---
        eco_text = row.get("ecosystem_hypothesis")
        eco_success = False

        if eco_text:
            print(f" -> [{t_id}] Step 1: Evaluating Ecosystem...")
            eco_payload = {"team_id": t_id, "hypothesis_type": "Ecosystem", "hypothesis": eco_text}
            eco_resp = httpx.post(f"{BASE_URL}/hypothesis/evaluate", json=eco_payload, headers=headers)
            
            if eco_resp.status_code == 200:
                task_id = eco_resp.json()["task_id"]
                hyp_id = eco_resp.json()["hypothesis_id"]

                # Poll for Ecosystem Completion
                for _ in range(30): # 30s timeout for AI
                    status = httpx.get(f"{BASE_URL}/hypothesis/status/{task_id}").json().get("status")
                    if status == "SUCCESS":
                        # Verify it's actually in the results route
                        res = httpx.get(f"{BASE_URL}/hypothesis/results/{hyp_id}")
                        if res.status_code == 200:
                            eco_success = True
                            f.write(f"  [ECOSYSTEM] SUCCESS - Score: {res.json().get('hypotheses_output_score')}\n")
                            f.write(f"  RESULT: {res.json().get('hypotheses_output')[:200]}...\n")
                            break
                    time.sleep(1)
        
        if not eco_success:
            f.write("  [ECOSYSTEM] FAILED or MISSING. Skipping Customer evaluation.\n")
            f.write("-" * 50 + "\n\n")
            print(f" !! [{t_id}] Ecosystem failed. Skipping Customer.")
            return # Exit this test row early

        # --- STEP B: CUSTOMER HYPOTHESIS (Only if eco_success is True) ---
        cust_text = row.get("customer_hypothesis")
        if cust_text:
            print(f" -> [{t_id}] Step 2: Ecosystem verified. Evaluating Customer...")
            cust_payload = {"team_id": t_id, "hypothesis_type": "Customer", "hypothesis": cust_text}
            cust_resp = httpx.post(f"{BASE_URL}/hypothesis/evaluate", json=cust_payload, headers=headers)
            
            if cust_resp.status_code == 200:
                c_task_id = cust_resp.json()["task_id"]
                c_hyp_id = cust_resp.json()["hypothesis_id"]

                for _ in range(30):
                    c_status = httpx.get(f"{BASE_URL}/hypothesis/status/{c_task_id}").json().get("status")
                    if c_status == "SUCCESS":
                        c_res = httpx.get(f"{BASE_URL}/hypothesis/results/{c_hyp_id}")
                        if c_res.status_code == 200:
                            f.write(f"  [CUSTOMER] SUCCESS - Score: {c_res.json().get('hypotheses_output_score')}\n")
                            f.write(f"  RESULT: {c_res.json().get('hypotheses_output')[:200]}...\n")
                            break
                    time.sleep(1)

        f.write("-" * 50 + "\n\n")