import streamlit as st
from helpers import add_message, render_chat, back, clear_chat

generic_answers = {
    "what is investment?": "Investment means putting money into assets to grow your wealth over time.",
    "how to open an account?": "Visit any of our branches or use our online portal to open an account.",
    "what are the fees?": "Fees depend on your account type. Basic accounts have zero monthly fees.",
    "what is ESG ETF?": "ESG ETFs invest in companies focusing on environmental, social, and governance practices.",
    "how do I check my balance?": "You can check your balance via our mobile app or online banking portal.",
    "how to contact support?": "Email support@hsbc.com or call 1800-HSBC-HELP (24/7).",
}

visitor_questions_stage_0 = [
    ("What is investment?", "what is investment?"),
    ("How to open an account?", "how to open an account?"),
    ("What are the fees?", "what are the fees?"),
]

visitor_questions_stage_1 = [
    ("What is ESG ETF?", "what is ESG ETF?"),
    ("How do I check my balance?", "how do I check my balance?"),
    ("How to contact support?", "how to contact support?"),
]

def visitor():
    if not st.session_state.chat_history:
        add_message("assistant", "Hi! 👋 How can I help you today?")
        st.session_state.chat_stage = 0

    render_chat()

    if st.session_state.chat_stage == 0:
        cols = st.columns(3)
        for i, (label, key) in enumerate(visitor_questions_stage_0):
            with cols[i]:
                if st.button(label, key=f"visitor_q0_{i}"):
                    add_message("user", key)
                    add_message("assistant", generic_answers[key])
                    st.session_state.chat_stage = 1
                    st.rerun()

    elif st.session_state.chat_stage == 1:
        cols = st.columns(3)
        for i, (label, key) in enumerate(visitor_questions_stage_1):
            with cols[i]:
                if st.button(label, key=f"visitor_q1_{i}"):
                    add_message("user", key)
                    add_message("assistant", generic_answers[key])
                    # stay in stage 1 or optionally reset to 0
                    st.rerun()

    back()
# Add Footer
st.markdown("---")  # Horizontal line for separation
footer_cols = st.columns([1, 1])

with footer_cols[0]:
    if st.button("Accessibility Options"):
        st.info("Accessibility options will be available soon.")  # Or add actual feature

