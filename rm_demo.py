import streamlit as st
from helpers import add_message, render_chat, back, load_css, speak_text

rm_answers_set_1 = {
    "show client list": "Clients: Alex Tan, Brian Lim, Clara Wong.",
    "recommend portfolio": "A balanced portfolio with ETFs and bonds fits most clients seeking moderate growth.",
    "how to contact clients?": "Use the CRM dashboard or email for client communication.",
}

rm_answers_set_2 = {
    "onboard new client": "Guide them through the e-KYC process and submit necessary documentation.",
    "portfolio performance": "Access each client profile to view their portfolio trend charts and performance reports.",
    "client meetings": "Schedule meetings using the integrated calendar tool in the CRM.",
}

def rm():
    load_css()
    render_chat()

    if "rm_stage" not in st.session_state:
        st.session_state.rm_stage = 0

    if not st.session_state.get("rm_welcome_shown", False):
        add_message("assistant", f"Welcome, RM {st.session_state.username} 👩‍💼 How can I assist you today?")
        st.session_state.rm_welcome_shown = True

    if st.session_state.rm_stage == 0:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Show Client List"):
                add_message("user", "show client list")
                add_message("assistant", rm_answers_set_1["show client list"])
                speak_text(rm_answers_set_1["show client list"])
                st.session_state.rm_stage = 1
                st.rerun()
        with col2:
            if st.button("Recommend Portfolio"):
                add_message("user", "recommend portfolio")
                add_message("assistant", rm_answers_set_1["recommend portfolio"])
                speak_text(rm_answers_set_1["recommend portfolio"])
                st.session_state.rm_stage = 1
                st.rerun()
        with col3:
            if st.button("How to Contact Clients?"):
                add_message("user", "how to contact clients?")
                add_message("assistant", rm_answers_set_1["how to contact clients?"])
                speak_text(rm_answers_set_1["how to contact clients?"])
                st.session_state.rm_stage = 1
                st.rerun()

    elif st.session_state.rm_stage == 1:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Onboard New Client"):
                add_message("user", "onboard new client")
                add_message("assistant", rm_answers_set_2["onboard new client"])
                speak_text(rm_answers_set_2["onboard new client"])
                st.session_state.rm_stage = 2
                st.rerun()
        with col2:
            if st.button("Portfolio Performance"):
                add_message("user", "portfolio performance")
                add_message("assistant", rm_answers_set_2["portfolio performance"])
                speak_text(rm_answers_set_2["portfolio performance"])
                st.session_state.rm_stage = 2
                st.rerun()
        with col3:
            if st.button("Client Meetings"):
                add_message("user", "client meetings")
                add_message("assistant", rm_answers_set_2["client meetings"])
                speak_text(rm_answers_set_2["client meetings"])
                st.session_state.rm_stage = 2
                st.rerun()

    back(stage_key="rm_stage")
