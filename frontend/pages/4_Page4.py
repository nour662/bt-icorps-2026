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


st.title("User Persona Recommendation (NOT COMPLETED YET)")

container = st.container()
with container:

    st.info(" ### How to use this page \n " \
    "1. Select your Hypothesis from the dropdown\n " \
    "2. Click the 'Evaluate User Persona' button.\n " \
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

                    time.sleep(3)
