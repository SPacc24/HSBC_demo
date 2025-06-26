import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from helpers import add_message, render_chat, back, logout, load_css, speak_text

load_css()

product_prices = pd.DataFrame({
    "date": pd.date_range(start="2025-01-01", periods=6, freq="M"),
    "ESG ETF": [100, 102, 105, 107, 110, 115],
    "Green Bonds": [100, 101, 101.5, 102, 102.5, 103]
})

persona_products = {
    "Cautious": ["Green Bonds"],
    "Growth": ["ESG ETF", "Balanced Fund"],
    "Aggressive": ["Tech ETF", "Crypto Index"]
}

customer_answers = {
    "what is my portfolio?": "Your portfolio contains ESG ETF (50%), Balanced Fund (30%), and Green Bonds (20%).",
    "how risky is my portfolio?": "Your portfolio risk level is Medium, balancing growth and safety.",
    "can i change my risk level?": "Yes, you can adjust your risk tolerance anytime via the app or your RM."
}

def predict_future(prices):
    x = np.arange(len(prices)).reshape(-1, 1)
    y = np.array(prices).reshape(-1, 1)
    model = LinearRegression()
    model.fit(x, y)
    future_x = np.arange(len(prices), len(prices) + 3).reshape(-1, 1)
    predictions = model.predict(future_x)
    return predictions.flatten().tolist()

def customer():
    render_chat()

    if not st.session_state.welcome_shown:
        add_message("assistant", f"Welcome back, {st.session_state.username}! How can I help you today?")
        st.session_state.welcome_shown = True

    if st.session_state.chat_stage == 0:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("What is my portfolio?"):
                add_message("user", "what is my portfolio?")
                add_message("assistant", customer_answers["what is my portfolio?"])
                speak_text(customer_answers["what is my portfolio?"])
                st.session_state.chat_stage = 1
                st.rerun()
        with col2:
            if st.button("How risky is my portfolio?"):
                add_message("user", "how risky is my portfolio?")
                add_message("assistant", customer_answers["how risky is my portfolio?"])
                speak_text(customer_answers["how risky is my portfolio?"])
                st.session_state.chat_stage = 1
                st.rerun()
        with col3:
            if st.button("Can I change my risk level?"):
                add_message("user", "can i change my risk level?")
                add_message("assistant", customer_answers["can i change my risk level?"])
                speak_text(customer_answers["can i change my risk level?"])
                st.session_state.chat_stage = 1
                st.rerun()

    elif st.session_state.chat_stage == 1:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Compare ESG ETF vs Green Bonds"):
                add_message("user", "Compare ESG ETF vs Green Bonds")
                latest_prices = product_prices.iloc[-1][["ESG ETF", "Green Bonds"]]
                msg = f"Current Prices:\n- ESG ETF: {latest_prices['ESG ETF']}\n- Green Bonds: {latest_prices['Green Bonds']}"
                add_message("assistant", msg)
                speak_text(msg)
                esg_future = predict_future(product_prices["ESG ETF"].tolist())
                gb_future = predict_future(product_prices["Green Bonds"].tolist())
                forecast = f"Predicted prices (next 3 months):\n- ESG ETF: {[f'{p:.2f}' for p in esg_future]}\n- Green Bonds: {[f'{p:.2f}' for p in gb_future]}"
                add_message("assistant", forecast)
                speak_text(forecast)
                st.session_state.chat_stage = 2
                st.rerun()
        with col2:
            if st.button("See historical trends"):
                add_message("user", "See historical trends")
                fig = px.line(product_prices, x="date", y=["ESG ETF", "Green Bonds"], title="Historical Product Prices")
                add_message("assistant", fig)
                st.session_state.chat_stage = 2
                st.rerun()
        with col3:
            if st.button("Recommendations by Persona"):
                persona = st.session_state.get("persona", "Cautious")
                recommendations = persona_products.get(persona, [])
                add_message("user", "Show me recommendations")
                rec_msg = f"Based on your profile (**{persona}**), we recommend: {', '.join(recommendations)}"
                add_message("assistant", rec_msg)
                speak_text(rec_msg)
                st.session_state.chat_stage = 2
                st.rerun()

    back()
    logout()
