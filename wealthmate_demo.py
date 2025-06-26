import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="WealthMate Demo", layout="wide")

# --- Fake user database ---
users = {
    "alex": {"password": "client123", "role": "Customer", "persona": "Cautious"},
    "cheryl": {"password": "rm123", "role": "Relationship Manager"},
}

# --- Fake product tracking data ---
product_prices = pd.DataFrame({
    "date": pd.date_range(start="2025-01-01", periods=6, freq="M"),
    "ESG ETF": [100, 102, 105, 107, 110, 115],
    "Green Bonds": [100, 101, 101.5, 102, 102.5, 103]
})

# --- Persona-based product gating ---
persona_products = {
    "Cautious": ["Green Bonds"],
    "Growth": ["ESG ETF", "Balanced Fund"],
    "Aggressive": ["Tech ETF", "Crypto Index"]
}

# --- Session state setup ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Helper: respond to Q ---
def respond_to_question(question, role):
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
    if role == "Visitor":
        return generic_answers.get(question, "Sorry, I don't know the answer to that yet.")
    elif role == "Customer":
        return customer_answers.get(question, "Sorry, I cannot answer that right now.")
    elif role == "Relationship Manager":
        return rm_answers.get(question, "Sorry, I don't have that info.")
    return "Unknown role."

# --- Login ---
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
            st.rerun()
        else:
            st.error("Invalid credentials.")

def logout():
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.chat_history = []
        st.rerun()

# --- Visitor mode ---
def normal_visitor():
    st.chat_message("assistant").markdown("Hi! What do you want to know today?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💸 What is investment?"):
            st.chat_message("user").markdown("What is investment?")
            st.chat_message("assistant").markdown("Investment means putting money into assets to grow your wealth over time.")
    with col2:
        if st.button("🏦 Open an account"):
            st.chat_message("user").markdown("How to open an account?")
            st.chat_message("assistant").markdown("Visit any of our branches or use our online portal to open an account.")
    with col3:
        if st.button("📋 Fees"):
            st.chat_message("user").markdown("What are the fees?")
            st.chat_message("assistant").markdown("Fees depend on your account type. Basic accounts have zero monthly fees.")

# --- Customer mode ---
def customer():
    st.chat_message("assistant").markdown(f"Welcome back, {st.session_state.username}!")

    st.subheader("📊 Portfolio Tracking")
    fig = px.line(product_prices, x="date", y=product_prices.columns[1:], title="Product Price Trends")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("💬 Ask about your investments")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📈 My portfolio"):
            st.chat_message("user").markdown("What is my portfolio?")
            st.chat_message("assistant").markdown("Your portfolio contains ESG ETF (50%), Balanced Fund (30%), and Green Bonds (20%).")
    with col2:
        if st.button("⚖️ Risk level"):
            st.chat_message("user").markdown("How risky is my portfolio?")
            st.chat_message("assistant").markdown("Your portfolio risk level is Medium, balancing growth and safety.")
    with col3:
        if st.button("🛠 Change risk level"):
            st.chat_message("user").markdown("Can I change my risk level?")
            st.chat_message("assistant").markdown("Yes, you can adjust your risk tolerance anytime via the app or your RM.")

    persona = users[st.session_state.username].get("persona", "Cautious")
    st.subheader("🔐 Recommended Products")
    allowed = persona_products.get(persona, [])
    for prod in allowed:
        st.markdown(f"- ✅ {prod}")

    logout()

# --- Relationship Manager mode ---
def rm():
    st.chat_message("assistant").markdown(f"Welcome, RM {st.session_state.username} 👩‍💼")

    st.subheader("👥 Clients")
    st.write("1. Alex Tan")
    st.write("2. Brian Lim")
    st.write("3. Clara Wong")

    st.subheader("💬 RM Options")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Client list"):
            st.chat_message("user").markdown("Show client list")
            st.chat_message("assistant").markdown("Clients: Alex Tan, Brian Lim, Clara Wong.")
    with col2:
        if st.button("💼 Recommend"):
            st.chat_message("user").markdown("Recommend portfolio")
            st.chat_message("assistant").markdown("A balanced portfolio with ETFs and bonds fits most clients seeking moderate growth.")
    with col3:
        if st.button("📨 Contact clients"):
            st.chat_message("user").markdown("How to contact clients?")
            st.chat_message("assistant").markdown("Use the CRM dashboard or email for client communication.")

    logout()

# --- Main Flow ---
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
