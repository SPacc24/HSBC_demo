import streamlit as st
from helpers import add_message, render_chat, back, load_css

generic_answers = {
    "what is investment?": "Investment means putting money into assets to grow your wealth over time.",
    "how to open an account?": "Visit any of our branches or use our online portal to open an account.",
    "what are the fees?": "Fees depend on your account type. Basic accounts have zero monthly fees."
}

def visitor():
    load_css()
    if not st.session_state.chat_history:
        add_message("assistant", "Hi! 👋 How can I help you today?")
        st.session_state.chat_stage = 0

    render_chat()

    if st.session_state.chat_stage == 0:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("What is investment?"):
                add_message("user", "what is investment?")
                add_message("assistant", generic_answers["what is investment?"])
                st.session_state.chat_stage = 1
                st.rerun()
        with col2:
            if st.button("How to open an account?"):
                add_message("user", "how to open an account?")
                add_message("assistant", generic_answers["how to open an account?"])
                st.session_state.chat_stage = 1
                st.rerun()
        with col3:
            if st.button("What are the fees?"):
                add_message("user", "what are the fees?")
                add_message("assistant", generic_answers["what are the fees?"])
                st.session_state.chat_stage = 1
                st.rerun()

    back(stage_key="chat_stage")
