# main_app.py
import streamlit as st
from helpers import load_css
from visitor_demo import visitor
from client_demo import customer
from rm_demo import rm

# --- Load CSS for layout ---
load_css()

# --- Session state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.welcome_shown = False
if "chat_stage" not in st.session_state:
    st.session_state.chat_stage = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Fake user db ---
users = {
    "alex": {"password": "client123", "role": "Customer", "persona": "Cautious"},
    "cheryl": {"password": "rm123", "role": "Relationship Manager"},
}

# --- Footer ---
def render_footer():
    st.markdown("""
    <div class="footer">
        <div>🧑‍🦳 <a href='#' onclick="window.location.reload();" title='Toggle accessibility mode'>Accessibility</a></div>
        <div>📞 Need help? 1800-XXX-XXXX | 📧 support@hsbc.com | <a href='https://www.hsbc.com.sg/help/' target='_blank'>Help Center</a></div>
    </div>
    """, unsafe_allow_html=True)

# --- Login ---
def login():
    st.title("WealthMate Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.session_state.persona = users[username].get("persona", "Cautious")
            st.rerun()
        else:
            st.error("Invalid credentials.")

# --- Sidebar role selector (only if not logged in) ---
if not st.session_state.logged_in:
    role_option = st.sidebar.selectbox("🔐 Select your role", ["Visitor", "Customer", "Relationship Manager"])
    if role_option == "Visitor":
        visitor()
    else:
        login()
else:
    role = st.session_state.role
    if role == "Customer":
        customer()
    elif role == "Relationship Manager":
        rm()

# --- Always render footer ---
render_footer()
