import streamlit as st
import plotly.graph_objects as go
from helpers import add_message, render_chat, back

# Product data
products = {
    "unit_trust": {
        "name": "BGF World Gold A2 SGD-H (BWGS)",
        "risk": "High",
        "amount_range": (1000, 4999),
        "objective": "b",
        "info_link": "https://investments4.personal-banking.hsbc.com.sg/srbp/public/utb/en-gb/fundDetail/BWGS",
        "prices_forecast": [115, 116.5, 118.0],
    },
    "bond": {
        "name": "HSBC GIF Global Short Duration Bond ACH SGD (HGDSH)",
        "risk": "Low",
        "amount_range": (5100, 10000),
        "objective": "a",
        "info_link": "https://investments4.personal-banking.hsbc.com.sg/srbp/public/utb/en-gb/fundDetail/HGDSH",
        "prices_forecast": [103, 103.5, 104.0],
    }
}

# Portfolio info
portfolio = {
    "SGGSA": {"amount": 2000, "weight": 0.25, "return": 20.32, "sd": 38.66},
    "FEGS": {"amount": 6000, "weight": 0.75, "return": 3.52, "sd": 13.034},
    "current_return": 7.72
}

def weighted_return(weights, returns):
    return sum(w * r for w, r in zip(weights, returns))

def match_product(risk, objective, amount):
    matched = []
    for p_key, p in products.items():
        low, high = p["amount_range"]
        if (risk.lower() == p["risk"].lower() or (risk.lower() == "moderate" and p["risk"].lower() in ["low", "high"])) and \
           (objective.lower() == p["objective"]) and (low <= amount <= high):
            matched.append(p)
    return matched

def plot_forecast(product):
    months = ["Month 1", "Month 2", "Month 3"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=product["prices_forecast"], mode="lines+markers", name=product["name"]))
    fig.update_layout(
        title=f"3-Month Price Forecast for {product['name']}",
        yaxis_title="Price (SGD)",
        xaxis_title="Month",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_portfolio_comparison():
    current = portfolio["current_return"]
    new_return_bwgs = 8.52
    new_return_hgds = 5.12

    products_list = ["Current Portfolio", "Add BWGS (Unit Trust)", "Add HGDSH (Bond)"]
    returns_list = [current, new_return_bwgs, new_return_hgds]

    fig = go.Figure(data=[go.Bar(x=products_list, y=returns_list, text=[f"{r}%" for r in returns_list], textposition='auto')])
    fig.update_layout(title="Portfolio Return Comparison", yaxis_title="Return (%)", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

def customer():
    if "step" not in st.session_state:
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.chat_history = []
        st.session_state.show_forecast = None
        st.session_state.show_compare = False
        add_message("assistant", "Welcome! Let's build your investment profile.")
    
    render_chat()

    if st.session_state.step == 0:
        st.markdown("**What is your risk appetite?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Moderate", key="risk_mod"):
                st.session_state.answers["risk"] = "Moderate"
                add_message("user", "Moderate")
                add_message("assistant", "Noted: Moderate risk appetite.")
                st.session_state.step += 1
                st.rerun()
        with col2:
            if st.button("High", key="risk_high"):
                st.session_state.answers["risk"] = "High"
                add_message("user", "High")
                add_message("assistant", "Noted: High risk appetite.")
                st.session_state.step += 1
                st.rerun()

    elif st.session_state.step == 1:
        st.markdown("**Overall, which best describes your investment objectives?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("(a) Capital preservation", key="obj_a"):
                st.session_state.answers["objective"] = "a"
                add_message("user", "(a) Capital preservation")
                add_message("assistant", "Noted: Capital preservation.")
                st.session_state.step += 1
                st.rerun()
        with col2:
            if st.button("(b) High capital appreciation", key="obj_b"):
                st.session_state.answers["objective"] = "b"
                add_message("user", "(b) High capital appreciation")
                add_message("assistant", "Noted: High capital appreciation.")
                st.session_state.step += 1
                st.rerun()

    elif st.session_state.step == 2:
        st.markdown("**What is your wanted invested amount?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("1,000 – 5,000", key="amt_1"):
                st.session_state.answers["amount"] = 3000
                add_message("user", "1,000 – 5,000")
                add_message("assistant", "Noted investment amount: SGD 1,000 – 5,000.")
                st.session_state.step += 1
                st.rerun()
        with col2:
            if st.button("5,100 – 10,000", key="amt_2"):
                st.session_state.answers["amount"] = 7500
                add_message("user", "5,100 – 10,000")
                add_message("assistant", "Noted investment amount: SGD 5,100 – 10,000.")
                st.session_state.step += 1
                st.rerun()

    elif st.session_state.step == 3:
        matched_products = match_product(
            st.session_state.answers["risk"],
            st.session_state.answers["objective"],
            st.session_state.answers["amount"]
        )
        if matched_products:
            for product in matched_products:
                add_message(
                    "assistant",
                    f"Based on your profile, we recommend the product: **{product['name']}**\n"
                    f"Risk: {product['risk']}\n"
                    f"Investment amount: SGD {product['amount_range'][0]} – {product['amount_range'][1]}\n"
                    f"Objective: {'Capital preservation' if product['objective']=='a' else 'High capital appreciation'}\n"
                    f"[More info]({product['info_link']})"
                )
            st.session_state.step += 1
            st.rerun()
        else:
            add_message("assistant", "Sorry, no products match your profile exactly. Please contact your RM for advice.")
            st.session_state.step = 0
            st.rerun()

    elif st.session_state.step == 4:
        st.markdown("**Would you like to view more insights about your recommendation?**")

    # Safe matching only after step >= 3
    matched_product = None
    if st.session_state.step >= 3:
        matched_products = match_product(
            st.session_state.answers.get("risk", ""),
            st.session_state.answers.get("objective", ""),
            st.session_state.answers.get("amount", 0)
        )
        matched_product = matched_products[0] if matched_products else None

    col1, col2 = st.columns(2)
    if matched_product:
        with col1:
            if st.button(f"View Forecast: {matched_product['name']}", key="view_forecast"):
                add_message("user", f"View Forecast: {matched_product['name']}")
                add_message("assistant", f"Here is the 3-month forecast for {matched_product['name']}.")
                st.session_state.show_forecast = matched_product["name"]
                st.session_state.show_compare = False
                st.rerun()

    with col2:
        if st.button("Compare Portfolio Returns", key="compare_returns"):
            add_message("user", "Compare Portfolio Returns")
            add_message("assistant", "Here is the comparison of your portfolio returns with and without the new products.")
            st.session_state.show_compare = True
            st.session_state.show_forecast = None
            st.rerun()

    if st.session_state.show_forecast:
        forecast_product = next((p for p in products.values() if p["name"] == st.session_state.show_forecast), None)
        if forecast_product:
            plot_forecast(forecast_product)

    if st.session_state.show_compare:
        plot_portfolio_comparison()

    back()
