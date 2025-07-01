import streamlit as st
from helpers import add_message, render_chat, back

stage_0_questions = {
    "What is my portfolio return?": "Your current return on portfolio is **7.72%** based on your asset mix:\n\n- SGGSA: 25% (Return: 20.32%)\n- FEGS: 75% (Return: 3.52%)",
    "Show product recommendation": "Based on your profile:\n\n**BGF World Gold A2 SGD-H BWGS**\n- 🧭 Risk: High\n- 💰 Amount: $1k–4.9k\n- 🎯 Objective: High capital appreciation\n\n👉 [View Product Info](https://www.hsbc.com.sg/investments/products/unit-trusts/)",
    "Simulate new portfolio (add unit trust)": "📊 If you add **1k in BWGS**, your new return on portfolio is **8.52%**.\n\nBreakdown:\n- SGGSA: 2/9\n- FEGS: 2/3\n- BWGS: 1/9"
}

stage_1_questions = {
    "Simulate new portfolio (add bond)": "📉 If you add **8k in HGDSH**, your new return is **5.12%**.\n\nBreakdown:\n- SGGSA: 1/8\n- FEGS: 3/8\n- HGDSH: 1/2",
    "Compare BWGS vs HGDSH": (
        "**BGF World Gold A2 (BWGS)**\n- Risk: High | Return Potential: High\n- Objective: Capital appreciation\n\n"
        "**HSBC Global Short Duration Bond (HGDSH)**\n- Risk: Low | Return: Stable\n- Objective: Capital preservation"
    ),
}

def customer():
    if not st.session_state.chat_history:
        add_message("assistant", f"Welcome back, {st.session_state.username}! How can I help you today?")
        st.session_state.chat_stage = 0

    render_chat()

    if st.session_state.chat_stage == 0:
        cols = st.columns(3)
        for i, (q, _) in enumerate(stage_0_questions.items()):
            with cols[i]:
                if st.button(q.capitalize(), key=f"customer_q0_{i}"):
                    add_message("user", q)
                    add_message("assistant", stage_0_questions[q])
                    st.session_state.chat_stage = 1
                    st.rerun()

    elif st.session_state.chat_stage == 1:
        cols = st.columns(3)
        for i, (q, _) in enumerate(stage_1_questions.items()):
            with cols[i]:
                if st.button(q.capitalize(), key=f"customer_q1_{i}"):
                    add_message("user", q)
                    add_message("assistant", stage_1_questions[q])
                    st.rerun()

    back()
