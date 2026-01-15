import streamlit as st

# Colors from I-Corps PDF
# Navy: #213F6B | Light Blue: #6883A3 | Red: #CC2029 | Dark Gray: #262626

def apply_css():
    css = """
    <style>
        /* IMPORT FONTS: Roboto & Montserrat */
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Roboto:wght@700&display=swap');

        /* GLOBAL THEME OVERRIDES */
        h1, h2, h3 { font-family: 'Roboto', sans-serif; color: #E5E5E5; }
        p, div, button { font-family: 'Montserrat', sans-serif; color: #E5E5E5; }

        /* Card Style (Around the box) */
        .custom-card {
            background-color: #262626; /* Dark Gray Background */
            border: 2px solid #213F6B; /* Navy Blue Border */
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s, border-color 0.3s, box-shadow 0.3s;
            height: 100%;
        }
        .custom-card:hover {
            transform: translateY(-5px);
            border-color: #CC2029; /* Red Highlight on Hover */
            box-shadow: 0 0 15px rgba(204, 32, 41, 0.5); /* Red Glow */
        }
        
        /* BUTTON STYLING (On Click) */
        .stButton > button {
            background-color: #213F6B !important; /* Navy Blue */
            color: white !important;
            border-radius: 15px;
            border: none;
            width: 100%;
            font-weight: 600;
        }
        .stButton > button {
            transition: transform 0.2s ease, background-color 0.5s ease;
        }

        .stButton > button:hover {
            background-color: #CC2029 !important;
            transform: scale(1.1);
            color: white !important;
        }

        /* LOGIN BOX STYLING */
        .login-container {
            max-width: 400px;
            margin: auto;
            padding: 40px;
            background-color: #1E1E1E;
            border-top: 5px solid #CC2029; /* I-Corps Red Accent */
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)