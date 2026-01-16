import time
from sqlalchemy.orm import Session
from theme import i_corp_theme, sidebar
from css import apply_css
import streamlit as st
import plotly as px
import plotly.graph_objects as go
import requests
from streamlit_app import API_BASE

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
        hyp_selection = st.selectbox("Select your Hypothesis Type here:", ["","Ecosystem", "Customer"], key="hypothesis_type")
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
                    current_team = st.session_state.get("current_user")
                    req = requests.post(
                        f"{API_BASE}/hypothesis/evaluate",
                        json={
                            "team_id" : current_team,
                            "hypothesis_type" : hyp_selection,
                            "hypothesis" : hyp_details
                        },
                        timeout=30
                    )
                    req.raise_for_status()
                    res = req.json()
                    status = res["status"]
                    task_id = res["task_id"]
                    hypothesis_id = res["hypothesis_id"]
                    while (status != "SUCCESS"):
                        #This slows it down 
                        time.sleep(2.5)

                        req = requests.get(
                        f"{API_BASE}/hypothesis/status/{task_id}",
                        timeout=30
                        )
                        req.raise_for_status()
                        res = req.json()
                        status = res["status"]
                    req = requests.get(
                        f"{API_BASE}/hypothesis/results/{hypothesis_id}",
                        timeout=30
                    )
                    req.raise_for_status()
                    output_dict = req.json()
                    score = output_dict["hypotheses_output_score"]
                    output = output_dict["hypotheses_output"]

 # 3. Display the Gauge Chart (The "Wheel")
                    st.markdown("### Evaluation Score")
                    
                    # Create columns to center the chart and make it "half size"
                    # The middle column (col_center) is 2 parts, giving it roughly 50% width
                    col_left, col_center, col_right = st.columns([1, 2, 1])
                    
                    with col_center:
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = score,
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Confidence Score", 'font': {'size': 20, 'family': "Roboto"}},
                            number = {'font': {'size': 40, 'family': "Montserrat", 'color': "#262626"}},
                            gauge = {
                                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                                # Change bar color to I-Corps Navy so it fits the theme 
                                # and doesn't look like a generic "black bar"
                                'bar': {'color': "#213F6B", 'thickness': 0.25}, 
                                'bgcolor': "white",
                                'borderwidth': 2,
                                'bordercolor': "white",
                                'steps': [
                                    {'range': [0, 39], 'color': "#AD0606"},   # Dark Red
                                    {'range': [40, 64], 'color': "#FF4B4B"},  # Red
                                    {'range': [65, 80], 'color': "#FACA2B"},  # Yellow
                                    {'range': [81, 89], 'color': "#90EE90"},  # Light Green
                                    {'range': [90, 100], 'color': "#008000"}  # Dark Green
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 80
                                }
                            }
                        ))
                        # Reduce margin and height to make it compact
                        fig.update_layout(
                            height=250, 
                            margin=dict(l=20, r=20, t=50, b=20),
                            paper_bgcolor="rgba(0,0,0,0)", # Transparent background
                            font={'family': "Montserrat"}
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)

                    if score >= 80:
                        st.success(f"You have a Strong Hypothesis! (Score: {score})") #not sure if that is right or needed
                        # with st.spinner("Generating user personas..."):
                        # personas = generate_personas_function(h_desc)
                        # # st.write(personas)
                        #     pass
                        st.write(output)
                    else:
                        st.write("You have a Weak Hypothesis")
                        st.write(output)
                               
