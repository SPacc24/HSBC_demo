import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="WealthMate Demo", layout="wide")

# --- Fake user database ---
users = {
    "alex": {"password": "client123", "role": "Customer", "persona": "Cautious"},
    "cheryl": {"password": "rm123", "role": "Relationship Manager"},
}

# --- Predefined Q&A responses ---
generic_answers = {
    "what is investment?": "Investment means putting money into assets to grow your wealth over time.",
    "how to open an account?": "Visit any of our branches or use our online portal to open an account.",
    "what are the fees?": "Fees depend on your account type. Basic accounts have zero monthly fees.",
}

customer_answers = {
    "what is my portfolio?": "Your portfolio contains ESG ETF (50%), Balanced Fund (30%), and Green Bonds (20%).",
    "how risky is my portfolio?": "Your portfolio risk level is Medium, balancing growth and safety.",
    "can i change my risk level?": "Yes, you can adjust your risk tolerance anytime via the app or your RM.",
}

rm_answers = {
    "show client list": "Clients: Alex Tan, Brian Lim, Clara Wong.",
    "recommend portfolio": "A balanced portfolio with ETFs and bonds fits most clients seeking moderate growth.",
    "how to contact clients?": "Use the CRM dashboard or email for client communication.",
}

# --- Fake product tracking data ---
product_prices = pd.DataFrame({
    "date": pd.date_range(start="2025-01-01", periods=6, freq="M"),
    "ESG ETF": [100, 102, 105, 107, 110, 115],
    "Green Bonds": [100, 101, 101.5, 102, 102.5, 103]
})

# --- Persona-based product gating ---
persona_products = {
    "Cautious": ["Green Bonds"],
    "Growth": ["ESG ETF", "Balanced Fund"],
    "Aggressive": ["Tech ETF", "Crypto Index"]
}

# --- Session state defaults ---
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

# --- Accessibility CSS ---
def apply_accessibility():
    if st.session_state.accessibility_mode:
        st.markdown("""
        <style>
            button, .stButton > button {
                font-size: 20px !important;
                padding: 15px 25px !important;
            }
            .chat-message, .stMarkdown p {
                font-size: 20px !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("", unsafe_allow_html=True)

apply_accessibility()

# --- Predictive price forecast ---
def predict_future(prices):
    x = np.arange(len(prices)).reshape(-1,1)
    y = np.array(prices).reshape(-1,1)
    model = LinearRegression()
    model.fit(x,y)
    future_x = np.arange(len(prices), len(prices)+3).reshape(-1,1)
    preds = model.predict(future_x)
    return preds.flatten().tolist()

# --- Helpers to add/render chat ---
def add_message(role, content):
    st.session_state.chat_history.append((role, content))

def render_chat():
    for role, msg in st.session_state.chat_history:
        if isinstance(msg, str):
            st.chat_message(role).markdown(msg)
        else:
            st.chat_message(role).plotly_chart(msg)

# --- Logout ---
def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.chat_stage = 0
    st.session_state.chat_history = []
    st.session_state.welcome_shown = False
    st.rerun()

# --- Back ---
def back():
    if st.session_state.chat_stage > 0:
        st.session_state.chat_stage -= 1
        # Remove last 2 messages (user + assistant)
        if len(st.session_state.chat_history) >= 2:
            st.session_state.chat_history = st.session_state.chat_history[:-2]
        st.rerun()

# --- Login page ---
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

# --- Visitor chat ---
def visitor():
    if not st.session_state.welcome_shown:
        add_message("assistant", "Hi! 👋 How can I help you today?")
        st.session_state.welcome_shown = True

    render_chat()

    if st.session_state.chat_stage == 0:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("What is investment?"):
                add_message("user", "what is investment?")
                add_message("assistant", generic_answers["what is investment?"])
                st.session_state.chat_stage = 1
                st.rerun()
        with col2:
            if st.button("How to open an account?"):
                add_message("user", "how to open an account?")
                add_message("assistant", generic_answers["how to open an account?"])
                st.session_state.chat_stage = 1
                st.rerun()
        with col3:
            if st.button("What are the fees?"):
                add_message("user", "what are the fees?")
                add_message("assistant", generic_answers["what are the fees?"])
                st.session_state.chat_stage = 1
                st.rerun()

    elif st.session_state.chat_stage == 1:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Tell me more about investments"):
                add_message("user", "tell me more about investments")
                add_message("assistant", "Investments can include stocks, bonds, mutual funds, and more.")
                st.session_state.chat_stage = 2
                st.rerun()
        with col2:
            if st.button("How to manage fees?"):
                add_message("user", "how to manage fees?")
                add_message("assistant", "You can reduce fees by choosing fee-free accounts or investing in low-cost funds.")
                st.session_state.chat_stage = 2
                st.rerun()

    elif st.session_state.chat_stage == 2:
        if st.button("Back to start"):
            st.session_state.chat_stage = 0
            st.session_state.chat_history = []
            st.session_state.welcome_shown = False
            st.rerun()

    if st.session_state.chat_stage > 0:
        if st.button("⬅️ Back"):
            back()

# --- Customer chat ---
def customer():
    if not st.session_state.welcome_shown:
        add_message("assistant", f"Welcome back, {st.session_state.username}! How can I help you today?")
        st.session_state.welcome_shown = True

    render_chat()

    if st.session_state.chat_stage == 0:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("What is my portfolio?"):
                add_message("user", "what is my portfolio?")
                add_message("assistant", customer_answers["what is my portfolio?"])
                st.session_state.chat_stage = 1
                st.rerun()
        with col2:
            if st.button("How risky is my portfolio?"):
                add_message("user", "how risky is my portfolio?")
                add_message("assistant", customer_answers["how risky is my portfolio?"])
                st.session_state.chat_stage = 1
                st.rerun()
        with col3:
            if st.button("Can I change my risk level?"):
                add_message("user", "can i change my risk level?")
                add_message("assistant", customer_answers["can i change my risk level?"])
                st.session_state.chat_stage = 1
                st.rerun()

    elif st.session_state.chat_stage == 1:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Compare ESG ETF vs Green Bonds"):
                add_message("user", "compare ESG ETF vs Green Bonds")
                latest_prices = product_prices.iloc[-1][["ESG ETF", "Green Bonds"]]
                msg = f"Current Prices:\n- ESG ETF: {latest_prices['ESG ETF']}\n- Green Bonds: {latest_prices['Green Bonds']}"
                add_message("assistant", msg)
                esg_future = predict_future(product_prices["ESG ETF"].tolist())
                gb_future = predict_future(product_prices["Green Bonds"].tolist())
                forecast = f"Predicted prices (next 3 months):\n- ESG ETF: {['%.2f' % p for p in esg_future]}\n- Green Bonds: {['%.2f' % p for p in gb_future]}"
                add_message("assistant", forecast)
                st.session_state.chat_stage = 2
                st.rerun()
        with col2:
            if st.button("See historical trends"):
                add_message("user", "see historical trends")
                fig = px.line(product_prices, x="date", y=["ESG ETF", "Green Bonds"], title="Historical Product Prices")
                add_message("assistant", fig)
                st.session_state.chat_stage = 2
                st.rerun()
        with col3:
            if st.button("Recommendations by Persona"):
                persona = users[st.session_state.username].get("persona", "Cautious")
                recommendations = persona_products.get(persona, [])
                add_message("user", "recommendations by persona")
                add_message("assistant", f"Based on your profile (**{persona}**), we recommend: {', '.join(recommendations)}")
                st.session_state.chat_stage = 2
                st.rerun()

    elif st.session_state.chat_stage == 2:
        if st.button("Back to main menu"):
            st.session_state.chat_stage = 0
            st.session_state.chat_history = []
            st.session_state.welcome_shown = False
            st.rerun()

    if st.session_state.chat_stage > 0:
        if st.button("⬅️ Back"):
            back()

# --- Relationship Manager chat ---
def rm():
    if not st.session_state.welcome_shown:
        add_message("assistant", f"Welcome, RM {st.session_state.username} 👩‍💼 How can I help you today?")
        st.session_state.welcome_shown = True

    render_chat()

    if st.session_state.chat_stage == 0:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Show client list"):
                add_message("user", "show client list")
                add_message("assistant", rm_answers["show client list"])
                st.session_state.chat_stage = 1
                st.rerun()
        with col2:
            if st.button("Recommend portfolio"):
                add_message("user", "recommend portfolio")
                add_message("assistant", rm_answers["recommend portfolio"])
                st.session_state.chat_stage = 1
                st.rerun()
        with col3:
            if st.button("How to contact clients?"):
                add_message("user", "how to contact clients?")
                add_message("assistant", rm_answers["how to contact clients?"])
                st.session_state.chat_stage = 1
                st.rerun()

    elif st.session_state.chat_stage == 1:
        if st.button("Back to main menu"):
            st.session_state.chat_stage = 0
            st.session_state.chat_history = []
            st.session_state.welcome_shown = False
            st.rerun()

    if st.session_state.chat_stage > 0:
        if st.button("⬅️ Back"):
            back()

# --- Main App ---

# Accessibility toggle in sidebar
with st.sidebar:
    st.header("Settings")
    acc_mode = st.checkbox("Accessibility Mode (Larger text/buttons)", value=st.session_state.accessibility_mode)
    if acc_mode != st.session_state.accessibility_mode:
        st.session_state.accessibility_mode = acc_mode
        st.rerun()

    st.markdown("---")

    if st.session_state.logged_in:
        if st.button("Logout"):
            logout()

role_option = st.sidebar.selectbox("🔐 Select your role", ["Visitor", "Customer", "Relationship Manager"])

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
