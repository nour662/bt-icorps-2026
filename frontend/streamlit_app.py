import streamlit as st
import time
from sqlalchemy.orm import Session
from theme import i_corp_theme, sidebar
from css import apply_css
import streamlit as st

i_corp_theme()  
apply_css()       
sidebar() 

#THESE THINGS ARE COMMENTED OUT FOR NOW
# from app.core.db.database import SessionLocal  # Adjust import based on your actual db file
# from app.models import Team
# from app.api.endpoints.auth_helper.password_security import verify_password
# from app.api.endpoints.auth_helper import create_access_token

#TO RUN the file to do: streamlit run frontend/streamlit_app.py


st.set_page_config(
    page_title="I-Corps Project Dashboard",
    page_icon="🚀", #This is going to be updated with Mtech ventures or umd logo
    layout="wide",
    initial_sidebar_state="collapsed"
)


# # --- 2. AUTHENTICATION LOGIC ---
# if "authenticated" not in st.session_state:
#     st.session_state["authenticated"] = False
# if "current_user" not in st.session_state:
#     st.session_state["current_user"] = None

# def attempt_login(username, password):
#     """
#     Connects to your existing backend to verify credentials.
#     """
#     db = SessionLocal() # Manually open a session since we aren't in a FastAPI route
#     try:
#         # Assuming your Team model has a 'username' or 'email' field. Adjust 'team_name' as needed.
#         team = db.query(Team).filter(Team.team_name == username).first() 
        
#         if not team:
#             st.error("Team not found.")
#             return False
            
#         # Verify Password using your existing security file
#         if verify_password(password, team.hashed_password):
#             st.session_state["authenticated"] = True
#             st.session_state["current_user"] = team.team_name
            
#             # Optional: Generate token if you need it for API calls later
#             token = create_access_token(team.team_id)
#             st.session_state["token"] = token
#             return True
#         else:
#             st.error("Incorrect password.")
#             return False
#     except Exception as e:
#         st.error(f"Login Error: {e}")
#         return False
#     finally:
#         db.close() # Always close the session

# # 3. LOGIN SCREEN 
# def login_page():
#     # Centering strategy using columns
#     c1, c2, c3 = st.columns([1, 2, 1])
    
#     with c2:
#         #adds some space at the top of the login box what unsafe_allow_html=True does is allow html code to be used in streamlit
#         st.markdown("<br><br>", unsafe_allow_html=True)  
#         st.markdown('<div class="login-container">', unsafe_allow_html=True)
#         st.title("I-Corps Login")
#         st.write("Please sign in to access the dashboard.")
        
#         username_input = st.text_input("Team Name")
#         password_input = st.text_input("Password", type="password")
        
#         if st.button("Login", key="login_btn"):
#             if attempt_login(username_input, password_input):
#                 st.rerun() # Reload to show dashboard
        
#         st.markdown('</div>', unsafe_allow_html=True)

def main_dashboard():     

    # Main Content Area
    st.markdown("<h1 style='text-align: center; color: #CC2029;'>Project Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Select a module to begin your I-Corps journey.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 3-Column Layout with "Card" Styling
    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

    # --- CARD 1: Hypothesis ---
    with col1:
        # We start a container to group elements visually (imitating a card)
        with st.container(border=True): 
            st.markdown("<h3 style='text-align: center;'>Hypothesis Evaluation</h3>", unsafe_allow_html=True)
            # Display Image
            #st.image("https://placehold.co/600x400/213F6B/FFF?text=Hypothesis", use_container_width=True)
            st.markdown("<p style='text-align: center; font-size: 0.9em;'>Get your businesses Ecosystem and Customer hypotheses scored and user persona recommendations with AI assistance.</p>", unsafe_allow_html=True)
            
            # The Button triggers the navigation
            if st.button("Go to Module ➔", key="btn1"):
                st.switch_page("pages/1_Page1.py") # MUST match actual filename in 'pages' folder

    # --- CARD 2: User Persona ---
    with col2:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center;'>User Persona</h3>", unsafe_allow_html=True)
            #st.image("https://placehold.co/600x400/6883A3/FFF?text=Personas", use_container_width=True)
            st.markdown("<p style='text-align: center; font-size: 0.9em;'>Assess user personas and get tailored interview question suggestions.</p>", unsafe_allow_html=True)
            
            if st.button("Go to Module ➔", key="btn2"):
                st.switch_page("pages/2_Page2.py")

    # --- CARD 3: Interviews ---
    with col3:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center;'>Interview Analysis</h3>", unsafe_allow_html=True)
            #st.image("https://placehold.co/600x400/CC2029/FFF?text=Analysis", use_container_width=True)
            st.markdown("<p style='text-align: center; font-size: 0.9em;'>Analyze interview transcripts for insights and alignment with goals.</p>", unsafe_allow_html=True)
            
            if st.button("Go to Module ➔", key="btn3"):
                st.switch_page("pages/3_Page3.py")


# # --- 5. CONTROL FLOW ---
# if not st.session_state["authenticated"]:
#     login_page()
# else:
#     main_dashboard()
main_dashboard()





