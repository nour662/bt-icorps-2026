import time
from sqlalchemy.orm import Session
from theme import i_corp_theme, sidebar
from css import apply_css
import streamlit as st
# from backend.app.worker.hyp_evaluation import evaluate_hypothesis_task
# from backend.app.core.db import SessionLocal

i_corp_theme()  
apply_css()       
sidebar() 


st.title("Hypothesis Evaluation and User Persona Recommendation")

container = st.container()
with container:

    st.info(" ### How to use this page \n " \
    "1. Input your hypothesis type and description in the fields above.\n " \
    "2. Click the 'Evaluate Hypothesis' button to receive an evaluation and score.\n " \
    "3. Based on your hypothesis, user persona recommendations will be provided IF the hypothesis is a score 80 or higher.\n " \
    "4. Use the recommendations to refine your hypotheses and better understand your target users.")

    #Form to fill in information such as hypothesis type and hypothesis
    st.form_key = "hypothesis_form"
    with st.form(key=st.form_key):
        hyp_selection = st.selectbox("Select your Hypothesis Type here:", ["","Ecosystem Hypothesis", "Customer Hypothesis"], key="hypothesis_type")
        hyp_details = st.text_area("Enter your Hypothesis here:", key="hypothesis_description")
        submitted = st.form_submit_button(label="Evaluate Hypothesis")

        #If the submit button is pressed to evaluate the hypothesis
        #Checks to see if there are any missing fields 
        if submitted: 
            if not hyp_details and hyp_selection:
                st.warning("### Please enter your Hypothesis Type and Hypothesis")
            elif not hyp_details:
                st.warning("### Please enter a Hypothesis first.")
            elif not hyp_selection:
                st.warning("### Please enter your Hypothesis type first")
                
                #If there are no missing fields then the evaluate_hypothesis_task will begin 
            else:
                # db = SessionLocal()
                #Loading animation because anlysis is not instant 
                with st.spinner("Analyzing your Hypothesis"):

                    #gets the current session that is in right now 
                    current_team = st.session_state.get("current_user", "test_team")

                    # try: 
                    #     result = evaluate_hypothesis_task(
                    #     hypothesis_id=1, 
                    #     hypothesis_text=hyp_details, 
                    #     hypothesis_type=hyp_selection, 
                    #     team_id=current_team
                    #     )


                        # score = result.get('score', 0) 
                        # feedback_text = result.get('feedback', "No feedback provided.")
                        # st.success("Analysis Complete!")


                    # except Exception as e: 
                    #     st.error(f"Backend Error: {e}")
                    #     score = 0
                    #     feedback_text = "Error occurred."
                    # finnaly:
                    # # db.close()
                                
            #have the score show colors on a wheel like red if its low yellow if its like 65-79 and light green then green then dark green for 80-89 90-99 and 100
            # if score >= 80:
            #     st.success("You have a Strong Hypothesis")
            #     with st.spinner("Generating user personas..."):
                # personas = generate_personas_function(h_desc)
            #     # st.write(personas)
            #         pass
            # else:
            #     st.feedback("You have a Weak Hypothesis")
