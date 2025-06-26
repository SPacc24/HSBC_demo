# rm_demo.py
import streamlit as st
from helpers import logout

rm_answers = {
    "show client list": "Clients: Alex Tan, Brian Lim, Clara Wong.",
    "recommend portfolio": "A balanced portfolio with ETFs and bonds fits most clients seeking moderate growth.",
    "how to contact clients?": "Use the CRM dashboard or email for client communication.",
    "how to onboard new client?": "Guide them through the e-KYC process and submit necessary documentation.",
    "view portfolio performance": "Access each client profile to view their portfolio trend charts and performance reports."
}

def rm():
    if not st.session_state.chat_history:
        st.session_state.chat_history = [("assistant", f"Welcome, RM {st.session_state.username} 👩‍💼 How can I assist you today?")]

    for role, msg in st.session_state.chat_history:
        st.chat_message(role).markdown(msg)

    for q in rm_answers:
        if st.button(q.capitalize()):
            st.chat_message("user").markdown(q)
            st.chat_message("assistant").markdown(rm_answers[q])

    logout()
