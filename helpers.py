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
        else:
            st.chat_message(role).plotly_chart(msg)

def back():
    if st.button("⬅️ Back") and st.session_state.chat_stage > 0:
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
        st.experimental_set_query_params()  # Clear query params (forces sidebar to reset)
        st.rerun()

def logout_button_footer():
    # We will use this in footer (return button markup for footer)
    return """
        <button id="logout-btn" style="
            background-color:#0072f5; border:none; color:#fff; padding:6px 14px; border-radius:5px;
            font-weight:600; font-size:0.9rem; cursor:pointer;">Logout</button>
        <script>
        const logoutBtn = window.parent.document.querySelector('#logout-btn');
        if(logoutBtn){
            logoutBtn.onclick = () => {
                window.parent.postMessage({type: 'streamlit:run'}, '*');
            };
        }
        </script>
    """

def speak_text(text):
    # JS snippet to run text-to-speech on given text
    escaped_text = text.replace('"', '\\"').replace('\n',' ')
    js = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{escaped_text}");
    msg.rate = 1;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)
