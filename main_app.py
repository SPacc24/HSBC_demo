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
for key, default in {
    "logged_in": False,
    "role": None,
    "username": None,
    "chat_stage": 0,
    "chat_history": [],
    "welcome_shown": False,
    "accessibility_mode": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Accessibility toggle icon ---
def accessibility_toggle():
    acc_icon = "🧑‍🦳"  # or ♿
    acc_mode = st.session_state.accessibility_mode
    if st.sidebar.button(acc_icon):
        st.session_state.accessibility_mode = not acc_mode
        st.rerun()
    st.sidebar.markdown(f"**Accessibility mode:** {'On' if acc_mode else 'Off'}")

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

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h2 style='margin-bottom: 0.25rem;'>Settings ⚙️</h2>", unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        role_option = st.selectbox("🔐 Select your role", ["Visitor", "Customer", "Relationship Manager"])
    else:
        role_option = st.session_state.role
        st.markdown(f"**Role:** {role_option}")

    # Accessibility toggle icon (no checkbox)
    acc_icon = "🧑‍🦳"
    acc_mode = st.session_state.accessibility_mode
    if st.button(acc_icon):
        st.session_state.accessibility_mode = not acc_mode
        st.rerun()
    st.markdown(f"**Accessibility mode:** {'On' if acc_mode else 'Off'}")

    # Support info box with theme-neutral style
    st.markdown(
        """
        <style>
        .support-box {
            padding: 12px;
            border-radius: 8px;
            background-color: var(--background, #f1f1f1);
            color: var(--text, #333);
            font-size: 14px;
            line-height: 1.4;
        }
        </style>
        <div class="support-box">
        Need help? Contact HSBC Support:<br>
        📞 Hotline: 1800-XXX-XXXX<br>
        📧 Email: support@hsbc.com<br>
        Or visit our <a href='https://www.hsbc.com.sg/help/' target='_blank'>Help Center</a>.
        </div>
        """, unsafe_allow_html=True
    )

    # Spacer pushes logout to bottom
    st.markdown("<div style='height: 140px;'></div>", unsafe_allow_html=True)

    # Logout button at bottom
    if st.session_state.logged_in:
        if st.button("🔒 Logout"):
            logout()

# --- Main app logic ---
if not st.session_state.logged_in or (st.session_state.role != role_option):
    login()
else:
    if role_option == "Visitor":
        visitor()
    elif role_option == "Customer":
        customer()
    elif role_option == "Relationship Manager":
        rm()
