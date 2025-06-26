import streamlit as st

def add_message(role, content):
    st.session_state.chat_history.append((role, content))

def render_chat():
    for role, msg in st.session_state.chat_history:
        if isinstance(msg, str):
            st.chat_message(role).markdown(msg)
        else:
            st.chat_message(role).plotly_chart(msg)

def clear_chat():
    st.session_state.chat_history = []
    st.session_state.chat_stage = 0

def back():
    if st.button("⬅️ Back", key="back_button") and st.session_state.chat_stage > 0:
        st.session_state.chat_stage -= 1
        # Remove last two messages (user+assistant)
        if len(st.session_state.chat_history) >= 2:
            st.session_state.chat_history = st.session_state.chat_history[:-2]
        st.rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.persona = None
    clear_chat()
    st.rerun()

def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
