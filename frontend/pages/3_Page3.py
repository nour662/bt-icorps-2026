import time
from sqlalchemy.orm import Session
from css import apply_css # Import the CSS styling
from theme import i_corp_theme, sidebar
from css import apply_css
import streamlit as st
import requests

from streamlit_app import API_BASE

i_corp_theme()  
apply_css()       
sidebar() 

st.title("Interview Analysis and Feedback")

container = st.container()
with container:

    st.info(" ### How to use this page \n " \
    "1. Upload the file of your interview transcript/notes. (make sure it is a PDF) and add any insights\n " \
    "2. Click the 'Analyze my interview' button to receive feedback.\n " \
    "3. CHANGE --> Based on your hypothesis, user persona recommendations will be provided IF the hypothesis is a score 80 or higher.\n " \
    "4. Use the recommendations to refine your interviews and better understand your target users.")

    #Form to fill in information such as hypothesis type and hypothesis
    st.form_key = "interview_form"
    with st.form(key=st.form_key):
        hyp_selection = st.file_uploader("Upload your interview here:", key="interview_upload")
        form_details = st.text_area("Enter your specific questions here (OPTIONAL):", key="interview_description")
        submitted = st.form_submit_button(label="Evaluate Interview")

        hypo_id = 1 # need hypo id for route
        
        #If the submit button is pressed to evaluate the hypothesis
        #Checks to see if there are any missing fields 
        if submitted: 
            if not hyp_selection:
                st.warning("### Please upload your interview")
                #If there are no missing fields then the evaluate_hypothesis_task will begin 
            else:
                # db = SessionLocal()
                #Loading animation because anlysis is not instant 
                with st.spinner("Analyzing your Hypothesis"):
                    try:
                        current_team = st.session_state.get("current_user") 
                        # presign_req = requests.post(
                        #     f"{API_BASE}/interview/presign",
                        #     json={
                        #         "filename": hyp_selection.name,
                        #         "content_type": "application/pdf"
                        #     },
                        #     timeout=30
                        # )
                        # presign_req.raise_for_status()
                        # presign_res = presign_req.json()
                        
                        # upload_url = presign_res["upload_url"]
                        # object_key = presign_res["object_key"]
                        
                        # upload_status = requests.put(
                        #     upload_url, 
                        #     data=hyp_selection.getvalue(),
                        #     headers={"Content-Type": "application/pdf"}
                        # )
                        # upload_status.raise_for_status()
                        
                        eval_req = requests.post(
                            f"{API_BASE}/interview/evaluate_interview",
                            json={
                                "hypothesis_id": hypo_id,
                                "s3_key": object_key
                            },
                            timeout=30
                        )  
                        
                        eval_req.raise_for_status()
                        eval_res = eval_req.json()
                        
                        task_id = eval_res["task_id"]
                        interview_id = eval_res["interviewee_id"]
                        status = eval_res["status"]
                        
                        while status != "SUCCESS":
                            time.sleep(2.5)
                            status_check = requests.get(f"{API_BASE}/interview/status/{task_id}")
                            status_check.raise_for_status()
                            status = status_check.json()["status"]
                        
                        # if exit loop, status is success    
                        result_res = requests.get(f"{API_BASE}/interview/result/{interview_id}")
                        result_res.raise_for_status()
                        output_dict = result_res.json()
                            
                        st.success("Analysis Complete!")
                        st.info(output_dict["summary"])
                            
                        st.write(output_dict["evaluation"])
                    except Exception as e:
                        st.error(f"Error!")
                    #gets the current session that is in right now 
                    # current_team = st.session_state.get("current_user")
                    # time.sleep(3)
                    # req = requests.post(
                    #     f"{API_BASE}/interview/application/pdf/presign",
                    #     json={
                    #         "team_id" : current_team,
                    #         "hypothesis_type" : hyp_selection,
                    #         "hypothesis" : hyp_details
                    #     },
                    #     timeout=30
                    # )
                    # req.raise_for_status()
                    # res = req.json()
                    # status = res["status"]
                    # task_id = res["task_id"]
                    # hypothesis_id = res["hypothesis_id"]
                    # while (status != "SUCCESS"):
                    #     req = requests.get(
                    #     f"{API_BASE}/hypothesis/status/{task_id}",
                    #     timeout=30
                    #     )
                    #     req.raise_for_status()
                    #     res = req.json()
                    #     status = res["status"]
                    # req = requests.get(
                    #     f"{API_BASE}/hypothesis/results/{hypothesis_id}",
                    #     timeout=30
                    # )
                    # req.raise_for_status()
                    # output_dict = req.json()
                    # score = output_dict["hypotheses_output_score"]
                    # output = output_dict["hypotheses_output"]
                    # st.write(output)