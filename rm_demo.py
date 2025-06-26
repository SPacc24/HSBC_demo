# rm_demo.py
import streamlit as st
from helpers import add_message, render_chat, back, logout, load_css

load_css()

rm_answers = {
    "show client list": "Clients: Alex Tan, Brian Lim, Clara Wong.",
    "recommend portfolio": "A balanced portfolio with ETFs and bonds fits most clients seeking moderate growth.",
    "how to contact clients?": "Use the CRM dashboard or email for client communication.",
    "how to onboard new client?": "Guide them through the e-KYC process and submit necessary documentation.",
    "view portfolio performance": "Access each client profile to view their portfolio trend charts and performance reports."
}

def rm():
    render_chat()

    if not st.session_state.welcome_shown:
        add_message("assistant", f"Welcome, RM {st.session_state.username} 👩‍💼 How can I assist you today?")
        st.session_state.welcome_shown = True

    col1, col2, col3 = st.columns(3)
    buttons = list(rm_answers.keys())

    with col1:
        if st.button(buttons[0].capitalize()):
            add_message("user", buttons[0])
            add_message("assistant", rm_answers[buttons[0]])
            st.rerun()
    with col2:
        if st.button(buttons[1].capitalize()):
            add_message("user", buttons[1])
            add_message("assistant", rm_answers[buttons[1]])
            st.rerun()
    with col3:
        if st.button(buttons[2].capitalize()):
            add_message("user", buttons[2])
            add_message("assistant", rm_answers[buttons[2]])
            st.rerun()

    col4, col5 = st.columns(2)
    with col4:
        if st.button(buttons[3].capitalize()):
            add_message("user", buttons[3])
            add_message("assistant", rm_answers[buttons[3]])
            st.rerun()
    with col5:
        if st.button(buttons[4].capitalize()):
            add_message("user", buttons[4])
            add_message("assistant", rm_answers[buttons[4]])
            st.rerun()

    back()
    logout()
