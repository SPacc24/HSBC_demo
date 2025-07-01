import streamlit as st
from helpers import load_css, add_message, clear_chat, render_chat, back, logout
from visitor_demo import visitor
from client_demo import customer
from rm_demo import rm

st.set_page_config(page_title="WealthMate Demo", layout="wide")

users = {
    "alex": {"password": "client123", "role": "Customer", "persona": "Cautious"},
    "cheryl": {"password": "rm123", "role": "Relationship Manager"},
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.persona = None

if "chat_stage" not in st.session_state:
    st.session_state.chat_stage = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def login(role):
    st.title(f"{role} Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        if username in users and users[username]["password"] == password and users[username]["role"] == role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.username = username
            st.session_state.persona = users[username].get("persona", None)
            clear_chat()
            st.success(f"Logged in as {username} ({role})")
            st.rerun()
        else:
            st.error("Invalid credentials.")

def render_footer():
    footer_style = """
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(250,250,250,0.95);
        color: #222;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        font-size: 0.9rem;
        box-shadow: 0 -2px 8px rgba(0,0,0,0.1);
        z-index: 9999;
        gap: 10px;
    """

    col1, col2, col3 = st.columns([1, 6, 3], gap="small")

    with col1:
        if st.button("Accessibility: OFF", key="accessibility_toggle"):
            # Removed accessibility toggle for now
            pass

    with col2:
        st.markdown(
            """
            <div style="text-align:center;">
            HSBC WealthMate Demo &mdash; For support, email <a href="mailto:support@hsbc.com">support@hsbc.com</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        if st.session_state.logged_in:
            if st.button("Logout", key="logout_button"):
                logout()

    st.markdown(f"<style>.footer {{{footer_style}}}</style>", unsafe_allow_html=True)
    st.markdown('<div class="footer"></div>', unsafe_allow_html=True)

def main():
    load_css()

    if not st.session_state.logged_in:
        role_option = st.sidebar.selectbox("Select your role", ["Visitor", "Customer", "Relationship Manager"])
        if role_option == "Visitor":
            visitor()
        elif role_option == "Customer":
            login("Customer")
        elif role_option == "Relationship Manager":
            login("Relationship Manager")
    else:
        if st.session_state.role == "Customer":
            customer()
        elif st.session_state.role == "Relationship Manager":
            rm()

    render_footer()

if __name__ == "__main__":
    main()
