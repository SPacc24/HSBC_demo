import streamlit as st
from helpers import add_message, render_chat, back

customer_answers_stage_0 = {
    "what is my portfolio?": "Your portfolio contains ESG ETF (50%), Balanced Fund (30%), and Green Bonds (20%).",
    "how risky is my portfolio?": "Your portfolio risk level is Medium, balancing growth and safety.",
    "can i change my risk level?": "Yes, you can adjust your risk tolerance anytime via the app or your RM.",
}

customer_answers_stage_1 = {
    "compare ESG ETF vs Green Bonds": (
        "Current Prices:\n- ESG ETF: 115\n- Green Bonds: 103\n"
        "Predicted prices (next 3 months):\n- ESG ETF: 116.5, 118.0, 119.5\n- Green Bonds: 103.5, 104.0, 104.5"
    ),
    "see historical trends": "You can view the price history on your dashboard under 'Market Trends'.",
    "recommendations by persona": "Based on your profile, we recommend a balanced mix of ESG ETFs and Green Bonds."
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
                    add_message("assistant", customer_answers_stage_0[q])
                    st.session_state.chat_stage = 1
                    st.rerun()

    elif st.session_state.chat_stage == 1:
        cols = st.columns(3)
        for i, (q, _) in enumerate(customer_answers_stage_1.items()):
            with cols[i]:
                if st.button(q.capitalize(), key=f"customer_q1_{i}"):
                    add_message("user", q)
                    add_message("assistant", customer_answers_stage_1[q])
                    # Stay in stage 1
                    st.rerun()

    back()
# Add Footer
st.markdown("---")  # Horizontal line for separation
footer_cols = st.columns([1, 1])

with footer_cols[0]:
    if st.button("Accessibility Options", key="footer_accessibility"):
        st.info("Accessibility options will be available soon.")

with footer_cols[1]:
    if st.button("Log Out", key="footer_logout"):
        from helpers import logout
        logout()
