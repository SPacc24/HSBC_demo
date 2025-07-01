### ai_logic.py

PRODUCTS = [
    {
        "name": "BGF World Gold A2 USD BWGU",
        "risk": "High",
        "amount_range": "SGD 1,000 – 10,000",
        "objective": "High capital appreciation",
        "summary": "A unit trust focused on gold-related companies with strong growth potential.",
        "link": "https://www.hsbc.com.sg/investments/products/unit-trusts/fund-details/"
    },
    # Add more products here
]

def match_products(profile):
    matched = []
    for product in PRODUCTS:
        if (product["risk"].lower() == profile["risk"].lower() and
            product["objective"].lower() in profile["objective"].lower() and
            product["amount_range"] == profile["amount"]):
            matched.append(product)
    return matched


def predict_prices_for(product_name):
    import numpy as np
    import pandas as pd
    from sklearn.linear_model import LinearRegression

    history = {
        "BGF World Gold A2 USD BWGU": [5.1, 5.3, 5.5, 5.6, 5.8, 6.0]
    }

    prices = history.get(product_name)
    if not prices:
        return None

    X = np.array(range(1, len(prices)+1)).reshape(-1, 1)
    y = np.array(prices)

    model = LinearRegression()
    model.fit(X, y)

    future_months = np.array([[7], [8], [9]])
    forecast = model.predict(future_months)

    df = pd.DataFrame({
        "Month": ["Month 7", "Month 8", "Month 9"],
        "Predicted Price": forecast
    })
    return df


### client_demo.py

import streamlit as st
from helpers import add_message, render_chat, back
from ai_logic import match_products, predict_prices_for
import plotly.express as px

customer_answers_stage_0 = {
    "show investment recommendation": "",  # to be filled with logic
    "predict product price": "",  # to be filled with logic
    "how risky is my portfolio?": "Your portfolio risk level is Medium, balancing growth and safety.",
}

def customer():
    if not st.session_state.chat_history:
        add_message("assistant", f"Welcome back, {st.session_state.username}! How can I help you today?")
        st.session_state.chat_stage = 0

    render_chat()

    if st.session_state.chat_stage == 0:
        cols = st.columns(3)
        for i, (q, _) in enumerate(customer_answers_stage_0.items()):
            with cols[i]:
                if st.button(q.capitalize(), key=f"customer_q0_{i}"):
                    add_message("user", q)

                    if q == "show investment recommendation":
                        profile = {
                            "risk": st.session_state.persona or "Moderate",
                            "objective": "High capital appreciation",
                            "amount": "SGD 1,000 – 10,000"
                        }
                        recs = match_products(profile)
                        if recs:
                            for p in recs:
                                msg = f"**{p['name']}**\n\n{p['summary']}\n\n[View more]({p['link']})"
                                add_message("assistant", msg)
                        else:
                            add_message("assistant", "Sorry, no matching products found.")

                    elif q == "predict product price":
                        df = predict_prices_for("BGF World Gold A2 USD BWGU")
                        if df is not None:
                            fig = px.line(df, x="Month", y="Predicted Price", title="Forecast for BGF World Gold")
                            add_message("assistant", fig)
                        else:
                            add_message("assistant", "No historical data available.")

                    else:
                        add_message("assistant", customer_answers_stage_0[q])

                    st.session_state.chat_stage = 1
                    st.rerun()

    back()