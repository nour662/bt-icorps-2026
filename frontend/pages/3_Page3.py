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