import streamlit as st
from helpers import add_message, render_chat, back

visitor_questions_stage_0 = [
    ("What is investment?", "Investment means putting money into assets to grow your wealth."),
    ("How to open an account?", "Click the button below to sign up for an HSBC account."),
    ("What are the fees?", "Fees vary based on your account type. Everyday Global has no monthly fee."),
]

visitor_questions_stage_1 = [
    ("What is ESG ETF?", "ESG ETFs invest in companies focused on environmental and social governance."),
    ("How do I check my balance?", "Use the HSBC mobile app or online banking."),
    ("How to contact HSBC?", "Visit hsbc.com.sg or call 1800-HSBC-HELP."),
]

def visitor():
    if not st.session_state.chat_history:
        add_message("assistant", "Hi! 👋 How can I help you today?")
        st.session_state.chat_stage = 0

    render_chat()

    if st.session_state.chat_stage == 0:
        cols = st.columns(3)
        for i, (label, response) in enumerate(visitor_questions_stage_0):
            with cols[i]:
                if st.button(label, key=f"visitor_q0_{i}"):
                    add_message("user", label)
                    add_message("assistant", response)
                    st.session_state.chat_stage = 1
                    st.rerun()

        st.markdown("### 🔗 Open an Account")
        st.markdown("[Open HSBC Bank Account](https://www.hsbc.com.sg/accounts/products/everyday-global-account/)")
        st.markdown("[Open Investment Account](https://www.hsbc.com.sg/log-on/)")

    elif st.session_state.chat_stage == 1:
        cols = st.columns(3)
        for i, (label, response) in enumerate(visitor_questions_stage_1):
            with cols[i]:
                if st.button(label, key=f"visitor_q1_{i}"):
                    add_message("user", label)
                    add_message("assistant", response)
                    st.rerun()

    back()
