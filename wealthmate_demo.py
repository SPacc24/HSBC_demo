import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
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

# --- Session state setup ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

if "chat_stage" not in st.session_state:
    st.session_state.chat_stage = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Predictive Analysis Helper ---
def predict_future(prices):
    x = np.arange(len(prices)).reshape(-1, 1)
    y = np.array(prices).reshape(-1, 1)
    model = LinearRegression()
    model.fit(x, y)
    future_x = np.arange(len(prices), len(prices) + 3).reshape(-1, 1)
    predictions = model.predict(future_x)
    return predictions.flatten().tolist()

# --- Add message to history ---
def add_message(role, content):
    st.session_state.chat_history.append((role, content))

# --- Render Chat ---
def render_chat():
    for role, msg in st.session_state.chat_history:
        if isinstance(msg, str):
            st.chat_message(role).markdown(msg)
        else:
            st.chat_message(role).plotly_chart(msg)

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
            st.rerun()
        else:
            st.error("Invalid credentials.")

def logout():
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.chat_stage = 0
        st.session_state.chat_history = []
        st.rerun()

# --- Back Button ---
def back():
    if st.button("⬅️ Back") and st.session_state.chat_stage > 0:
        st.session_state.chat_stage -= 1
        st.session_state.chat_history.append(("user", "Back"))
        st.rerun()

# --- Visitor chat ---
def visitor():
    st.chat_message("assistant").markdown("Hi! I’m WealthMate. Ask me anything about investments or banking services.")
    for q in generic_answers:
        if st.button(q.capitalize()):
            st.chat_message("user").markdown(q)
            st.chat_message("assistant").markdown(generic_answers[q])

# --- Customer chat ---
def customer():
    render_chat()

    if st.session_state.chat_stage == 0:
        add_message("assistant", f"Welcome back, {st.session_state.username}! Let's explore your personalized wealth journey.")
        add_message("assistant", "How can I assist you today?")
        for q in customer_answers:
            if st.button(q.capitalize()):
                add_message("user", q)
                add_message("assistant", customer_answers[q])
                st.session_state.chat_stage = 1
                st.rerun()

    elif st.session_state.chat_stage == 1:
        add_message("assistant", "Would you like to compare products or view forecasts?")
        if st.button("Compare ESG ETF vs Green Bonds"):
            add_message("user", "Compare ESG ETF vs Green Bonds")
            latest_prices = product_prices.iloc[-1][["ESG ETF", "Green Bonds"]]
            msg = f"Current Prices:\n- ESG ETF: {latest_prices['ESG ETF']}\n- Green Bonds: {latest_prices['Green Bonds']}"
            add_message("assistant", msg)
            esg_future = predict_future(product_prices["ESG ETF"].tolist())
            gb_future = predict_future(product_prices["Green Bonds"].tolist())
            forecast = f"Predicted future prices (next 3 months):\n- ESG ETF: {['%.2f' % p for p in esg_future]}\n- Green Bonds: {['%.2f' % p for p in gb_future]}"
            add_message("assistant", forecast)
            st.session_state.chat_stage = 2
            st.rerun()

        if st.button("See historical trends"):
            add_message("user", "See historical trends")
            fig = px.line(product_prices, x="date", y=["ESG ETF", "Green Bonds"], title="Historical Product Prices")
            add_message("assistant", fig)
            st.session_state.chat_stage = 2
            st.rerun()

        if st.button("Recommendations by Persona"):
            persona = users[st.session_state.username].get("persona", "Cautious")
            recommendations = persona_products.get(persona, [])
            add_message("user", "Show me recommendations")
            add_message("assistant", f"Based on your profile (**{persona}**), we recommend: {', '.join(recommendations)}")
            st.session_state.chat_stage = 2
            st.rerun()
        back()

    elif st.session_state.chat_stage == 2:
        add_message("assistant", "Would you like help making changes or viewing more projections?")
        back()

    logout()

# --- Relationship Manager chat ---
def rm():
    st.chat_message("assistant").markdown(f"Welcome, RM {st.session_state.username} 👩‍💼")
    for q in rm_answers:
        if st.button(q.capitalize()):
            st.chat_message("user").markdown(q)
            st.chat_message("assistant").markdown(rm_answers[q])
    logout()

# --- Main App Logic ---
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
