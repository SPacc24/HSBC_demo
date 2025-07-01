import streamlit as st
from helpers import add_message, render_chat, back
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime

# Sample products data (could be loaded from a DB or JSON)
products = [
    {
        "name": "BGF World Gold A2 USD BWGU",
        "type": "Unit trust",
        "risk_appetite": "High",
        "investment_amount_range": (1000, 4999),
        "investment_objective": "High capital appreciation",
        "description": "Global gold fund focused on capital growth.",
        "link": "https://www.hsbc.com.sg/investments/unit-trusts/bgfwgu"
    },
    {
        "name": "Green Bonds",
        "type": "Bond",
        "risk_appetite": "Moderate",
        "investment_amount_range": (1000, 100000),
        "investment_objective": "Stable income",
        "description": "Bonds financing environmentally friendly projects.",
        "link": "https://www.hsbc.com.sg/investments/green-bonds"
    },
    # Add more products as needed
]

# Mapping answers to internal terms
risk_map = {
    "Moderate": "Moderate",
    "High": "High",
}

objective_map = {
    "(a) Capital preservation": "Capital preservation",
    "(b) A regular stream of stable income": "Stable income",
    "(c) A combination of income and capital growth": "Combination",
    "(d) High capital appreciation": "High capital appreciation",
}

investment_amount_ranges = [
    (1000, 10000),
    (11000, 20000),
    (21000, 50000),
    (51000, 100000),
    (100001, 10**9)  # Large number for "More than 100,000"
]

def recommend_products(risk, objective, amount):
    matched = []
    for p in products:
        # Match risk
        if p["risk_appetite"] != risk:
            continue
        # Match objective loosely
        if objective not in p["investment_objective"]:
            # allow partial matches for combination cases
            if objective == "Combination" and "combination" in p["investment_objective"].lower():
                pass
            else:
                continue
        # Match investment amount
        low, high = p["investment_amount_range"]
        if low <= amount <= high:
            matched.append(p)
    return matched

def generate_forecast():
    # Simulate 12 months of prices with a simple increasing trend + noise
    dates = pd.date_range(start=datetime.date.today(), periods=12, freq='M')
    prices = 100 + np.cumsum(np.random.randn(12) * 2 + 1)  # trend with noise

    df = pd.DataFrame({'date': dates, 'price': prices})

    # Prepare data for linear regression
    X = np.arange(len(df)).reshape(-1, 1)
    y = df['price'].values

    model = LinearRegression()
    model.fit(X, y)
    forecast_X = np.arange(len(df) + 3).reshape(-1, 1)
    forecast_y = model.predict(forecast_X)

    forecast_dates = pd.date_range(start=df['date'].iloc[0], periods=len(forecast_y), freq='M')

    forecast_df = pd.DataFrame({'date': forecast_dates, 'forecast_price': forecast_y})
    return df, forecast_df

def customer():
    if "chat_stage" not in st.session_state:
        st.session_state.chat_stage = 0
    if not st.session_state.chat_history:
        add_message("assistant", f"Welcome back, {st.session_state.username}! How can I help you today?")
        st.session_state.chat_stage = 0

    render_chat()

    if st.session_state.chat_stage == 0:
        risk = st.selectbox("What is your risk appetite?", ["Moderate", "High"])
        objective = st.selectbox("Which best describes your investment objectives?", list(objective_map.keys()))
        amount_str = st.selectbox("What is your wanted invested amount?", [
            "1,000 – 10,000",
            "11,000 – 20,000",
            "21,000 - 50,000",
            "51,000 - 100,000",
            "More than 100,000"
        ])

        invest_amount = int(amount_str.split("–")[0].replace(",", "").strip() if "More than" not in amount_str else "100001")

        if st.button("Get Recommendations"):
            selected_risk = risk_map[risk]
            selected_objective = objective_map[objective]
            matched_products = recommend_products(selected_risk, selected_objective, invest_amount)
            if not matched_products:
                add_message("assistant", "Sorry, no products match your profile exactly. Please try different options.")
            else:
                msg = "Here are products matched to your profile:\n"
                for p in matched_products:
                    msg += f"\n**{p['name']}** ({p['type']})\n"
                    msg += f"Description: {p['description']}\n"
                    msg += f"[More info]({p['link']})\n"
                add_message("assistant", msg)
            st.session_state.chat_stage = 1
            st.experimental_rerun()

    elif st.session_state.chat_stage == 1:
        st.markdown("### Price Forecast Chart")
        hist_df, forecast_df = generate_forecast()
        import plotly.express as px
        fig = px.line(title="Historical and Forecasted Prices")
        fig.add_scatter(x=hist_df['date'], y=hist_df['price'], mode='lines+markers', name='Historical')
        fig.add_scatter(x=forecast_df['date'], y=forecast_df['forecast_price'], mode='lines', name='Forecast')
        st.plotly_chart(fig)
        back()
