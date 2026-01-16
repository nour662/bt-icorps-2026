import time
from sqlalchemy.orm import Session
from css import apply_css # Import the CSS styling
from theme import i_corp_theme, sidebar
from css import apply_css
import streamlit as st

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

                    #gets the current session that is in right now 
                    current_team = st.session_state.get("current_user")
                    time.sleep(3)
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