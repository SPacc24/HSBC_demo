import streamlit as st
from helpers import add_message, render_chat, back

rm_answers = {
    "show client list": "Clients: Alex Tan, Brian Lim, Clara Wong.",
    "recommend portfolio": "A balanced portfolio with ETFs and bonds fits most clients seeking moderate growth.",
    "how to contact clients?": "Use the CRM dashboard or email for client communication.",
}

def rm():
    if not st.session_state.welcome_shown:
        add_message("assistant", f"Welcome, RM {st.session_state.username} 👩‍💼 How can I help you today?")
        st.session_state.welcome_shown = True

    render_chat()

    if st.session_state.chat_stage == 0:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Show client list"):
                add_message("user", "show client list")
                add_message("assistant", rm_answers["show client list"])
                st.session_state.chat_stage = 1
                st.rerun()
        with col2:
            if st.button("Recommend portfolio"):
                add_message("user", "recommend portfolio")
                add_message("assistant", rm_answers["recommend portfolio"])
                st.session_state.chat_stage = 1
                st.rerun()
        with col3:
            if st.button("How to contact clients?"):
                add_message("user", "how to contact clients?")
                add_message("assistant", rm_answers["how to contact clients?"])
                st.session_state.chat_stage = 1
                st.rerun()

    elif st.session_state.chat_stage == 1:
        if st.button("Back to main menu"):
            st.session_state.chat_stage = 0
            st.session_state.chat_history = []
            st.session_state.welcome_shown = False
            st.rerun()

    if st.session_state.chat_stage > 0:
        if st.button("⬅️ Back"):
            back()
