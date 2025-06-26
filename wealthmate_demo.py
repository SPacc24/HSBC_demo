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

# --- Predictive Analysis Helper ---
def predict_future(prices):
    x = np.arange(len(prices)).reshape(-1, 1)
    y = np.array(prices).reshape(-1, 1)
    model = LinearRegression()
    model.fit(x, y)
    future_x = np.arange(len(prices), len(prices) + 3).reshape(-1, 1)
    predictions = model.predict(future_x)
    return predictions.flatten().tolist()

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
        st.rerun()

# --- Back Button ---
def back():
    if st.button("⬅️ Back") and st.session_state.chat_stage > 0:
        st.session_state.chat_stage -= 1
        st.rerun()

# --- Customer chat simulation ---
def customer():
    st.chat_message("assistant").markdown(f"Welcome back, {st.session_state.username}! Let's explore your investments.")

    if st.session_state.chat_stage == 0:
        st.chat_message("assistant").markdown("How can I assist you today?")
        if st.button("📈 View Portfolio"):
            st.chat_message("user").markdown("View Portfolio")
            st.chat_message("assistant").markdown("Your portfolio: ESG ETF (50%), Balanced Fund (30%), Green Bonds (20%)")
            st.session_state.chat_stage = 1
            st.rerun()
        if st.button("⚖️ Portfolio Risk"):
            st.chat_message("user").markdown("Portfolio Risk")
            st.chat_message("assistant").markdown("Your portfolio risk is Medium. It balances growth and safety.")
            st.session_state.chat_stage = 1
            st.rerun()
        if st.button("🔄 Change Risk Level"):
            st.chat_message("user").markdown("Change Risk Level")
            st.chat_message("assistant").markdown("You can adjust your risk tolerance via the settings page or RM.")
            st.session_state.chat_stage = 1
            st.rerun()

    elif st.session_state.chat_stage == 1:
        st.chat_message("assistant").markdown("Would you like to explore product performance or ask more?")
        if st.button("📊 Compare ESG ETF vs Green Bonds"):
            st.chat_message("user").markdown("Compare ESG ETF vs Green Bonds")
            latest_prices = product_prices.iloc[-1][["ESG ETF", "Green Bonds"]]
            st.chat_message("assistant").markdown(f"Current Prices:\n- ESG ETF: {latest_prices['ESG ETF']}\n- Green Bonds: {latest_prices['Green Bonds']}")
            esg_future = predict_future(product_prices["ESG ETF"].tolist())
            gb_future = predict_future(product_prices["Green Bonds"].tolist())
            st.chat_message("assistant").markdown(f"Predicted future prices (next 3 months):\n- ESG ETF: {['%.2f' % p for p in esg_future]}\n- Green Bonds: {['%.2f' % p for p in gb_future]}")
            st.session_state.chat_stage = 2
            st.rerun()
        if st.button("📈 See historical trends"):
            st.chat_message("user").markdown("See historical trends")
            fig = px.line(product_prices, x="date", y=["ESG ETF", "Green Bonds"], title="Historical Product Prices")
            st.chat_message("assistant").plotly_chart(fig)
            st.session_state.chat_stage = 2
            st.rerun()
        if st.button("❓ Why this allocation?"):
            st.chat_message("user").markdown("Why this allocation?")
            st.chat_message("assistant").markdown("This mix is based on your medium risk profile, blending growth and security.")
            st.session_state.chat_stage = 2
            st.rerun()
        back()

    elif st.session_state.chat_stage == 2:
        st.chat_message("assistant").markdown("Let me know if you'd like to adjust your portfolio or explore other products.")
        back()

    logout()

# --- Relationship Manager ---
def rm():
    st.chat_message("assistant").markdown(f"Welcome, RM {st.session_state.username} 👩‍💼")
    st.write("Client list and management tools coming soon.")
    logout()

# --- Visitor ---
def visitor():
    st.chat_message("assistant").markdown("Hi! What would you like to learn about?")
    if st.button("💸 What is investment?"):
        st.chat_message("user").markdown("What is investment?")
        st.chat_message("assistant").markdown("Investment means putting money into assets to grow your wealth over time.")
    if st.button("🏦 How to open account"):
        st.chat_message("user").markdown("How to open account")
        st.chat_message("assistant").markdown("Visit any of our branches or use our online portal.")
    if st.button("📋 Fees"):
        st.chat_message("user").markdown("What are the fees?")
        st.chat_message("assistant").markdown("Basic accounts have zero monthly fees.")

# --- Main Flow ---
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
