import time
from sqlalchemy.orm import Session
from theme import i_corp_theme, sidebar
from css import apply_css
import streamlit as st

i_corp_theme()  
apply_css()       
sidebar() 

st.title("User Persona Evaluation and Interview Question Recommendation")