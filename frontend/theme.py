import streamlit as st

#what is this? 
from PIL import Image

def i_corp_theme():
    st.set_page_config(
        page_title="I-Corps Project Dashboard",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

# def main_dashboard():
#     st.set_page_config(
#         page_title="I-Corps Project Dashboard",
#         page_icon="🚀", #This is going to be updated with Mtech ventures or umd logo
#         layout="wide",
#         initial_sidebar_state="collapsed"
#     )

def sidebar(): 
        # Sidebar Navigation
    with st.sidebar:
        # 1. LOGO (Uncomment when you have the file)
        # st.image("app/frontend/static/logo.png", width=150)

        #FOR NOW USE THIS: 
        user = st.session_state.get("current_user", "Guest")
        st.title(f"Welcome, {user}")

        #USE THIS LATER WHEN THIS IS FIGURED OUT 
        # #st.title(f"Welcome, {st.session_state['current_user']}")

        st.markdown("---")
        st.page_link("streamlit_app.py", label="Home", icon="🏠")
        st.page_link("pages/1_Page1.py", label="Hypothesis Evaluation and User Persona Recommendation", icon="📄") 
        st.page_link("pages/2_Page2.py", label="User Persona Evaluation and Interview Question Recommendation", icon="👥")
        st.page_link("pages/3_Page3.py", label="Interview Analysis and Feedback", icon="📊")
        
        st.markdown("---")

        # #Might not be needed not sure how we will do autho, will figure that out on thursday
        # if st.button("Logout"):
        #     st.session_state["authenticated"] = False
        #     st.rerun()
