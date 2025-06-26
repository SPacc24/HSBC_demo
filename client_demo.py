import streamlit as st
import pandas as pd
import plotly.express as px
from helpers import add_message, render_chat, back, predict_future

product_prices = pd.DataFrame({
    "date": pd.date_range(start="2025-01-01", periods=6, freq="M"),
    "ESG ETF": [100, 102, 105, 107, 110, 115],
    "Green Bonds": [100, 101, 101.5, 102, 102.5, 103]
})

customer_answers = {
    "what is my portfolio?": "Your portfolio contains ESG ETF (50%), Balanced Fund (30%), and Green Bonds (20%).",
    "how risky is my portfolio?": "Your portfolio risk level is Medium, balancing growth and safety.",
    "can i change my risk level?": "Yes, you can adjust your risk tolerance anytime via the app or your RM.",
}

persona_products = {
    "Cautious": ["Green Bonds"],
    "Growth": ["ESG ETF", "Balanced Fund"],
    "Aggressive": ["Tech ETF", "Crypto Index"]
}

users = {
    "alex": {"persona": "Cautious"},
    # add more if needed
}

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
                persona = users.get(st.session_state.username, {}).get("persona", "Cautious")
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
