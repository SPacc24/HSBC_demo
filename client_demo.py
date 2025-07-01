import streamlit as st
import plotly.graph_objects as go
from helpers import add_message, render_chat, back

# Customer canned responses (simplified for demo)
customer_answers_stage_0 = {
    "what is my portfolio?": (
        "Your portfolio contains:\n"
        "- Schroder International Selection Fund Global Gold SGD Hedged Class A Acc (SGGSA) - SGD 2000 (25%)\n"
        "- FIDELITY EUROPEAN GROWTH FUND S$ - REINVEST DIVD (FEGS) - SGD 6000 (75%)\n"
        "Current Return on Portfolio: 7.72%"
    ),
    "how risky is my portfolio?": "Your portfolio risk level is Medium, balancing growth and safety.",
    "can i change my risk level?": "Yes, you can adjust your risk tolerance anytime via the app or your RM.",
}

customer_answers_stage_1 = {
    "forecast bwgs": "Showing 3-month forecast for BGF World Gold A2 SGD-H (BWGS).",
    "forecast hgds": "Showing 3-month forecast for HSBC GIF Global Short Duration Bond ACH SGD (HGDSH).",
    "compare portfolio": "Comparing current portfolio returns with addition of BWGS and HGDSH products.",
}

def plot_forecast(product_name, prices):
    months = ["Month 1", "Month 2", "Month 3"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=prices, mode="lines+markers", name=product_name))
    fig.update_layout(
        title=f"3-Month Price Forecast for {product_name}",
        yaxis_title="Price (SGD)",
        xaxis_title="Time",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_portfolio_comparison():
    # Current portfolio return
    current_return = 7.72
    # After adding BWGS (unit trust)
    bwgs_return = 8.52
    # After adding HGDSH (bond)
    hgds_return = 5.12

    products = ["Current Portfolio", "Add BWGS (Unit Trust)", "Add HGDSH (Bond)"]
    returns = [current_return, bwgs_return, hgds_return]

    fig = go.Figure(data=[go.Bar(x=products, y=returns, text=[f"{r}%" for r in returns], textposition='auto')])
    fig.update_layout(
        title="Portfolio Return Comparison",
        yaxis_title="Return (%)",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

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
                    add_message("assistant", customer_answers_stage_0[q])
                    st.session_state.chat_stage = 1
                    st.rerun()

    elif st.session_state.chat_stage == 1:
        cols = st.columns(3)
        # Add buttons for forecast and portfolio comparison
        buttons = [
            ("Forecast: BWGS", "forecast bwgs"),
            ("Forecast: HGDSH", "forecast hgds"),
            ("Compare Portfolio Returns", "compare portfolio"),
        ]
        for i, (label, key) in enumerate(buttons):
            with cols[i]:
                if st.button(label, key=f"customer_q1_{i}"):
                    add_message("user", key)
                    add_message("assistant", customer_answers_stage_1[key])
                    st.rerun()

        # Show charts depending on last user message
        if st.session_state.chat_history:
            last_msg = st.session_state.chat_history[-1]
            if last_msg[0] == "user":
                if last_msg[1] == "forecast bwgs":
                    # Example mock forecast prices
                    prices = [115, 116.5, 118.0]
                    plot_forecast("BGF World Gold A2 SGD-H (BWGS)", prices)
                elif last_msg[1] == "forecast hgds":
                    prices = [103, 103.5, 104.0]
                    plot_forecast("HSBC GIF Global Short Duration Bond ACH SGD (HGDSH)", prices)
                elif last_msg[1] == "compare portfolio":
                    plot_portfolio_comparison()

    back()
