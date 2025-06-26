# main_app.py
import streamlit as st
from visitor_demo import visitor
from client_demo import customer
from rm_demo import rm
from helpers import logout

# --- Users database ---
users = {
    "alex": {"password": "client123", "role": "Customer", "persona": "Cautious"},
    "cheryl": {"password": "rm123", "role": "Relationship Manager"},
}

# --- Session state setup ---
def init_session():
    defaults = {
        "logged_in": False,
        "role": None,
        "username": None,
        "chat_stage": 0,
        "chat_history": [],
        "welcome_shown": False,
        "accessibility_mode": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

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
            st.success(f"Logged in as {username} ({st.session_state.role})")
            st.session_state.chat_history = []
            st.session_state.chat_stage = 0
            st.session_state.welcome_shown = False
            st.rerun()
        else:
            st.error("Invalid credentials.")

# --- Footer ---
def render_footer():
    st.markdown("""
    <hr style='margin-top: 2rem;'>
    <div style='display: flex; justify-content: space-between; font-size: 0.9rem;'>
        <div>
            <a href='#' onclick="window.location.reload();" title='Toggle accessibility mode'>🧑‍🦳 Accessibility</a>
        </div>
        <div>
            📞 Need help? Contact HSBC Support:<br>
            📞 1800-XXX-XXXX | 📧 support@hsbc.com | <a href='https://www.hsbc.com.sg/help/' target='_blank'>Help Center</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Sidebar role lock ---
if not st.session_state.logged_in:
    role_option = st.sidebar.selectbox("🔐 Select your role", ["Visitor", "Customer", "Relationship Manager"])
else:
    role_option = st.session_state.role
    st.sidebar.markdown(f"**Role:** {role_option}")

# --- Main App Logic ---
if role_option == "Visitor":
    st.session_state.logged_in = False
    visitor()
elif role_option in ["Customer", "Relationship Manager"]:
    if not st.session_state.logged_in or st.session_state.role != role_option:
        login()
    else:
        if role_option == "Customer":
            customer()
        else:
            rm()

# --- Logout button (always on sidebar bottom) ---
with st.sidebar:
    st.markdown("""<div style='height: 100px;'></div>""", unsafe_allow_html=True)
    if st.session_state.logged_in:
        if st.button("🔒 Logout"):
            logout()

# --- Footer with accessibility and help info ---
render_footer()
