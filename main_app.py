import streamlit as st
from helpers import load_css, add_message, render_chat, logout, clear_chat, speak_text, back
from visitor_demo import visitor
from client_demo import customer
from rm_demo import rm

load_css()

users = {
    "alex": {"password": "client123", "role": "Customer", "persona": "Cautious"},
    "cheryl": {"password": "rm123", "role": "Relationship Manager"},
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.welcome_shown = False
    st.session_state.chat_stage = 0
    st.session_state.chat_history = []
    st.session_state.accessibility_mode = False  # default off

def toggle_accessibility():
    st.session_state.accessibility_mode = not st.session_state.accessibility_mode

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
            clear_chat()
            st.rerun()
        else:
            st.error("Invalid credentials.")

def render_footer():
    accessibility_text = "Accessibility: ON" if st.session_state.accessibility_mode else "Accessibility: OFF"
    # Use columns to separate nicely and enable wrapping on small screen via CSS
    cols = st.columns([1,4,1])
    with cols[0]:
        if st.button(accessibility_text):
            toggle_accessibility()
            st.experimental_rerun()
    with cols[1]:
        st.markdown(
            """
            <div style="text-align:center;">
            Need help? Call 1800-XXX-XXXX | <a href="mailto:support@hsbc.com">support@hsbc.com</a> | 
            <a href="https://www.hsbc.com.sg/help/" target="_blank" rel="noopener noreferrer">Help Center</a>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with cols[2]:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            clear_chat()
            st.rerun()

def main():
    if not st.session_state.logged_in:
        role = st.sidebar.selectbox("Select role", ["Visitor", "Customer", "Relationship Manager"])
        if role == "Visitor":
            visitor()
        else:
            login()
    else:
        if st.session_state.role == "Customer":
            customer()
        elif st.session_state.role == "Relationship Manager":
            rm()

    render_footer()

main()
