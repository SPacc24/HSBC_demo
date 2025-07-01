import streamlit as st
from helpers import add_message, render_chat, back
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px
import datetime

products = [
    {
        "name": "BGF World Gold A2 USD BWGU",
        "type": "Unit trust",
        "risk_appetite": "High",
        "amount_range": (1000, 4999),
        "objective": "High capital appreciation",
        "description": "Global gold fund focused on capital growth.",
        "link": "https://www.hsbc.com.sg/investments/unit-trusts/bgfwgu"
    },
    {
        "name": "HSBC GIF Global Short Duration Bond AC USD HGDUA",
        "type": "Bond",
        "risk_appetite": "Moderate",
        "amount_range": (5100, 10000),
        "objective": "Capital preservation",
        "description": "Short duration bond fund for low-risk capital protection.",
        "link": "https://www.hsbc.com.sg/investments/unit-trusts/hgdua"
    }
]

def recommend_products(risk, objective, amount):
    matched = []
    for p in products:
        if p["risk_appetite"].lower() != risk.lower():
            continue
        if p["objective"].lower() not in objective.lower():
            continue
        low, high = p["amount_range"]
        if low <= amount <= high:
            matched.append(p)
    return matched

def generate_forecast():
    dates = pd.date_range(start=datetime.date.today(), periods=12, freq='M')
    prices = 100 + np.cumsum(np.random.randn(12) * 2 + 1)
    df = pd.DataFrame({'date': dates, 'price': prices})
    X = np.arange(len(df)).reshape(-1, 1)
    y = df['price'].values
    model = LinearRegression()
    model.fit(X, y)
    forecast_X = np.arange(len(df) + 3).reshape(-1, 1)
    forecast_y = model.predict(forecast_X)
    forecast_dates = pd.date_range(start=df['date'].iloc[0], periods=len(forecast_y), freq='M')
    forecast_df = pd.DataFrame({'date': forecast_dates, 'forecast_price': forecast_y})
    return df, forecast_df

def render_dashboard():
    st.subheader("Product Dashboard")

    st.markdown("**Price Trend (Forecasted)**")
    hist_df, forecast_df = generate_forecast()
    fig = px.line(title="Price Forecast")
    fig.add_scatter(x=hist_df['date'], y=hist_df['price'], mode='lines+markers', name='Historical')
    fig.add_scatter(x=forecast_df['date'], y=forecast_df['forecast_price'], mode='lines', name='Forecast')
    st.plotly_chart(fig)

    st.markdown("**Morningstar Rating**: ★★★★☆")
    st.markdown("**Portfolio Holding**:")
    st.markdown("- **Schroder International Selection Fund Global Gold SGD Hedged Class A Acc SGGSA**")
    st.markdown("- **Current Investment**: SGD 2000")
    st.markdown("- **Weight**: 38.66%")

def customer():
    if "chat_stage" not in st.session_state:
        st.session_state.chat_stage = 0
    if not st.session_state.chat_history:
        add_message("assistant", f"Welcome back, {st.session_state.username}! How can I help you today?")
        st.session_state.chat_stage = 0

    render_chat()

    if st.session_state.chat_stage == 0:
        risk = st.selectbox("What is your risk appetite?", ["Moderate", "High"])
        objective = st.selectbox("Which best describes your investment objective?", [
            "(a) Capital preservation",
            "(b) High capital appreciation"
        ])
        amount_input = st.selectbox("Investment amount:", [
            "1,000 – 5,000",
            "5,100 – 10,000"
        ])

        amount = 1000 if "1,000" in amount_input else 5100

        if st.button("Get Recommendations"):
            risk_val = risk
            obj_val = "High capital appreciation" if "appreciation" in objective else "Capital preservation"
            matched = recommend_products(risk_val, obj_val, amount)
            if not matched:
                add_message("assistant", "No products matched your inputs. Try different values.")
            else:
                msg = "Matched products based on your profile:\n"
                for p in matched:
                    msg += f"\n**{p['name']}** ({p['type']})\n"
                    msg += f"{p['description']}\n"
                    msg += f"[More Info]({p['link']})\n"
                add_message("assistant", msg)
            st.session_state.chat_stage = 1
            st.rerun()

    elif st.session_state.chat_stage == 1:
        render_dashboard()
        back()
