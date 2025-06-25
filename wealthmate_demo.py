import streamlit as st
import plotly.express as px

st.set_page_config(page_title="WealthMate Demo", layout="wide")

# --- Fake user database ---
users = {
    "alex": {"password": "client123", "role": "Customer"},
    "cheryl": {"password": "rm123", "role": "Relationship Manager"},
}

# --- Prewritten Q&A ---
generic_answers = {
    "What is investment?": "Investment means putting money into assets to grow your wealth over time.",
    "How to open an account?": "Visit any of our branches or use our online portal to open an account.",
    "What are the fees?": "Fees depend on your account type. Basic accounts have zero monthly fees.",
}

customer_answers = {
    "What is my portfolio?": "Your portfolio contains ESG ETF (50%), Balanced Fund (30%), and Green Bonds (20%).",
    "How risky is my portfolio?": "Your portfolio risk level is Medium, balancing growth and safety.",
    "Can I change my risk level?": "Yes, you can adjust your risk tolerance anytime via the app or your RM.",
}

rm_answers = {
    "Show client list": "Clients: Alex Tan, Brian Lim, Clara Wong.",
    "Recommend portfolio": "A balanced portfolio with ETFs and bonds fits most clients seeking moderate growth.",
    "How to contact clients?": "Use the CRM dashboard or email for client communication.",
}

# --- Fake portfolio data ---
portfolio_data = {
    "ESG ETF": 50,
    "Balanced Fund": 30,
    "Green Bonds": 20,
}

# --- Session state setup ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

# --- Helper: respond to Q ---
def respond_to_question(question, role):
    if role == "Visitor":
        return generic_answers.get(question, "Sorry, I don't know the answer to that yet.")
    elif role == "Customer":
        return customer_answers.get(question, "Sorry, I cannot answer that right now.")
    elif role == "Relationship Manager":
        return rm_answers.get(question, "Sorry, I don't have that info.")
    return "Unknown role."

# --- Helper: login logic ---
def login():
    st.title("WealthMate Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.success(f"Logged in as {username} ({st.session_state.role})")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials.")

def logout():
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.experimental_rerun()

# --- Visitor mode ---
def normal_visitor():
    st.title("Welcome, Visitor 👋")
    st.subheader("💬 Ask a general question:")

    question = st.radio("Choose a question:", list(generic_answers.keys()))
    if question:
        answer = respond_to_question(question, "Visitor")
        st.markdown(f"**WealthMate:** {answer}")

# --- Customer mode ---
def customer():
    st.title(f"Welcome Customer {st.session_state.username} 🧍‍♂️")

    tabs = st.tabs(["💬 Ask a Question", "📊 Portfolio", "🧾 Explanation"])

    with tabs[0]:
        st.subheader("💬 Portfolio Questions")
        question = st.radio("Select:", list(customer_answers.keys()))
        if question:
            answer = respond_to_question(question, "Customer")
            st.markdown(f"**WealthMate:** {answer}")

    with tabs[1]:
        st.subheader("📊 Your Portfolio Breakdown")
        fig = px.pie(
            names=list(portfolio_data.keys()),
            values=list(portfolio_data.values()),
            title="Portfolio Allocation"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        st.subheader("🧾 Portfolio Explanation")
        st.markdown("""
        Your portfolio is designed for moderate risk and long-term growth:
        - **50% ESG ETF**: Sustainable companies.
        - **30% Balanced Fund**: Steady growth.
        - **20% Green Bonds**: Fixed income with environmental impact.
        """)

    logout()

# --- Relationship Manager mode ---
def rm():
    st.title(f"Welcome RM {st.session_state.username} 👩‍💼")

    tabs = st.tabs(["💬 Advisor Q&A", "👥 Client List"])

    with tabs[0]:
        st.subheader("Ask an advisory question:")
        question = st.radio("Select:", list(rm_answers.keys()))
        if question:
            answer = respond_to_question(question, "Relationship Manager")
            st.markdown(f"**WealthMate:** {answer}")

    with tabs[1]:
        st.subheader("👥 Your Clients")
        st.write("1. Alex Tan")
        st.write("2. Brian Lim")
        st.write("3. Clara Wong")

    logout()

# --- App Main Flow ---
role_option = st.sidebar.selectbox("🔐 Select your role", ["Visitor", "Customer", "Relationship Manager"])

if role_option == "Visitor":
    st.session_state.logged_in = False
    normal_visitor()

elif role_option in ["Customer", "Relationship Manager"]:
    if not st.session_state.logged_in or st.session_state.role != role_option:
        login()
    else:
        if role_option == "Customer":
            customer()
        else:
            rm()
