import streamlit as st
from helpers import add_message, render_chat, back

generic_answers = {
    "what is investment?": "Investment means putting money into assets to grow your wealth over time.",
    "how to open an account?": "Visit any of our branches or use our online portal to open an account.",
    "what are the fees?": "Fees depend on your account type. Basic accounts have zero monthly fees.",
}

def visitor():
    if not st.session_state.welcome_shown:
        add_message("assistant", "Hi! 👋 How can I help you today?")
        st.session_state.welcome_shown = True

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

    elif st.session_state.chat_stage == 1:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Tell me more about investments"):
                add_message("user", "tell me more about investments")
                add_message("assistant", "Investments can include stocks, bonds, mutual funds, and more.")
                st.session_state.chat_stage = 2
                st.rerun()
        with col2:
            if st.button("How to manage fees?"):
                add_message("user", "how to manage fees?")
                add_message("assistant", "You can reduce fees by choosing fee-free accounts or investing in low-cost funds.")
                st.session_state.chat_stage = 2
                st.rerun()

    elif st.session_state.chat_stage == 2:
        if st.button("Back to start"):
            st.session_state.chat_stage = 0
            st.session_state.chat_history = []
            st.session_state.welcome_shown = False
            st.rerun()

    if st.session_state.chat_stage > 0:
        if st.button("⬅️ Back"):
            back()
