import streamlit as st
from helpers import load_css, add_message, render_chat, logout, clear_chat
from visitor_demo import visitor
from client_demo import customer
from rm_demo import rm

load_css()

# Fake user db
users = {
    "alex": {"password": "client123", "role": "Customer", "persona": "Cautious"},
    "cheryl": {"password": "rm123", "role": "Relationship Manager"},
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.welcome_shown = False
    st.session_state.chat_stage = 0
    st.session_state.chat_history = []

def login():
    st.title("WealthMate Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.session_state.persona = users[username].get("persona", "Cautious")
            clear_chat()
            st.experimental_set_query_params()  # clear query params
            st.rerun()
        else:
            st.error("Invalid credentials.")

def logout_footer():
    # The logout button in footer with style & working
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        clear_chat()
        st.experimental_set_query_params()
        st.rerun()

def render_footer():
    st.markdown(
        """
        <div class="footer">
            <div class="footer-section">
                <span title="Toggle accessibility mode" id="accessibility-toggle" class="accessibility-toggle" role="button" tabindex="0" aria-label="Toggle Accessibility Mode">♿</span>
            </div>
            <div class="footer-section">
                Need help? Call 1800-XXX-XXXX | <a href="mailto:support@hsbc.com">support@hsbc.com</a> | <a href="https://www.hsbc.com.sg/help/" target="_blank" rel="noopener noreferrer">Help Center</a>
            </div>
            <div class="footer-section">
                <button id="logout-button" aria-label="Logout">Logout</button>
            </div>
        </div>

        <script>
        const accessibilityToggle = document.getElementById('accessibility-toggle');
        const logoutButton = document.getElementById('logout-button');

        accessibilityToggle.onclick = () => {
            window.parent.postMessage({type: 'toggleAccessibility'}, '*');
        };
        logoutButton.onclick = () => {
            window.parent.postMessage({type: 'logout'}, '*');
        };
        </script>
        """,
        unsafe_allow_html=True,
    )

def main():
    if not st.session_state.logged_in:
        role = st.sidebar.selectbox("Select role", ["Visitor", "Customer", "Relationship Manager"])
        if role == "Visitor":
            visitor()
        else:
            login()
    else:
        if st.session_state.role == "Customer":
            customer()
        elif st.session_state.role == "Relationship Manager":
            rm()

    render_footer()

main()

# Listen for window messages for accessibility toggle and logout (JS/Streamlit hack)
import streamlit.components.v1 as components
components.html(
    """
    <script>
    window.addEventListener('message', (event) => {
        if(event.data.type === 'toggleAccessibility'){
            let mode = localStorage.getItem('accessibilityMode');
            if(mode === 'on'){
                localStorage.setItem('accessibilityMode', 'off');
                alert('Accessibility mode OFF');
            } else {
                localStorage.setItem('accessibilityMode', 'on');
                alert('Accessibility mode ON');
            }
            window.location.reload();
        } else if(event.data.type === 'logout'){
            window.location.reload();
        }
    });
    </script>
    """,
    height=0,
    scrolling=False,
)
