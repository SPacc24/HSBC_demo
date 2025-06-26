import streamlit as st
from helpers import add_message, render_chat, back

rm_answers_stage_0 = {
    "show client list": "Clients: Alex Tan, Brian Lim, Clara Wong.",
    "recommend portfolio": "A balanced portfolio with ETFs and bonds fits most clients seeking moderate growth.",
    "how to contact clients?": "Use the CRM dashboard or email for client communication.",
}

rm_answers_stage_1 = {
    "client meeting tips": "Always understand client goals and tailor your portfolio recommendations accordingly.",
    "update client info": "You can update client info using the CRM portal under 'Client Profiles'.",
    "schedule follow-ups": "Use the CRM calendar or your email to schedule follow-up meetings.",
}

def rm():
    if not st.session_state.chat_history:
        add_message("assistant", f"Welcome, RM {st.session_state.username} 👩‍💼 How can I help you today?")
        st.session_state.chat_stage = 0

    render_chat()

    if st.session_state.chat_stage == 0:
        cols = st.columns(3)
        for i, (q, _) in enumerate(rm_answers_stage_0.items()):
            with cols[i]:
                if st.button(q.capitalize(), key=f"rm_q0_{i}"):
                    add_message("user", q)
                    add_message("assistant", rm_answers_stage_0[q])
                    st.session_state.chat_stage = 1
                    st.rerun()

    elif st.session_state.chat_stage == 1:
        cols = st.columns(3)
        for i, (q, _) in enumerate(rm_answers_stage_1.items()):
            with cols[i]:
                if st.button(q.capitalize(), key=f"rm_q1_{i}"):
                    add_message("user", q)
                    add_message("assistant", rm_answers_stage_1[q])
                    # stay at stage 1
                    st.rerun()

    back()
