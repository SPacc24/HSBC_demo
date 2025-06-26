import streamlit as st

def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def add_message(role, content):
    st.session_state.chat_history.append((role, content))

def render_chat():
    for role, msg in st.session_state.chat_history:
        if isinstance(msg, str):
            st.chat_message(role).markdown(msg)
            # If accessibility is on and role is assistant, read aloud
            if role == "assistant" and st.session_state.get("accessibility_mode", False):
                speak_text(msg)
        else:
            st.chat_message(role).plotly_chart(msg)

def back():
    # Add key for button and put inside container to keep layout stable
    if st.button("⬅️ Back", key="back_button") and st.session_state.chat_stage > 0:
        st.session_state.chat_stage -= 1
        st.session_state.chat_history = st.session_state.chat_history[:-2]
        st.rerun()

def clear_chat():
    st.session_state.chat_stage = 0
    st.session_state.chat_history = []
    st.session_state.welcome_shown = False

def logout():
    if st.button("🔒 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        clear_chat()
        st.rerun()

def speak_text(text):
    escaped_text = text.replace('"', '\\"').replace('\n', ' ')
    js = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{escaped_text}");
    msg.rate = 1;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)
