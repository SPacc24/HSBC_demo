import streamlit as st

def load_css():
    with open("styles.css") as f:
        css = f.read()
    if st.session_state.get("accessibility_mode", False):
        st.markdown(f"""
            <style>
            {css}
            .main > div:first-child {{
                font-size: 20px !important;
                line-height: 1.5 !important;
            }}
            .main button {{
                padding: 14px 24px !important;
                font-size: 18px !important;
            }}
            </style>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def add_message(role, content):
    st.session_state.chat_history.append((role, content))

def render_chat():
    for role, msg in st.session_state.chat_history:
        if isinstance(msg, str):
            st.chat_message(role).markdown(msg)
            # Speak if accessibility ON and assistant message
            if role == "assistant" and st.session_state.get("accessibility_mode", False):
                speak_text(msg)
        else:
            st.chat_message(role).plotly_chart(msg)

def back(stage_key="chat_stage"):
    if st.button("⬅️ Back", key=f"back_{stage_key}"):
        if st.session_state.get(stage_key, 0) > 0:
            st.session_state[stage_key] -= 1
            if len(st.session_state.chat_history) >= 2:
                st.session_state.chat_history = st.session_state.chat_history[:-2]
            st.rerun()

def clear_chat():
    st.session_state.chat_stage = 0
    st.session_state.rm_stage = 0
    st.session_state.chat_history = []
    st.session_state.welcome_shown = False
    st.session_state.rm_welcome_shown = False

def logout():
    # Removed from here, logout only in footer now
    pass

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
