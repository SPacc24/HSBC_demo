import streamlit as st

def add_message(role, content):
    st.session_state.chat_history.append((role, content))

def render_chat():
    for role, msg in st.session_state.chat_history:
        if isinstance(msg, str):
            try:
                st.chat_message(role).markdown(msg)
            except UnicodeEncodeError:
                safe_msg = msg.encode("ascii", "ignore").decode()
                st.chat_message(role).markdown(safe_msg)
        else:
            st.chat_message(role).plotly_chart(msg)

def clear_chat():
    st.session_state.chat_history = []
    st.session_state.chat_stage = 0

def back():
    if st.button("Back", key="back_button") and st.session_state.chat_stage > 0:
        st.session_state.chat_stage -= 1
        if len(st.session_state.chat_history) >= 2:
            st.session_state.chat_history = st.session_state.chat_history[:-2]
        st.experimental_rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.persona = None
    clear_chat()
    st.experimental_rerun()

def load_css():
    with open("styles.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
