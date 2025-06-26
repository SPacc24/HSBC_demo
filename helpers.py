import streamlit as st
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression

def predict_future(prices):
    x = np.arange(len(prices)).reshape(-1,1)
    y = np.array(prices).reshape(-1,1)
    model = LinearRegression()
    model.fit(x,y)
    future_x = np.arange(len(prices), len(prices)+3).reshape(-1,1)
    preds = model.predict(future_x)
    return preds.flatten().tolist()

def add_message(role, content):
    st.session_state.chat_history.append((role, content))

def render_chat():
    for role, msg in st.session_state.chat_history:
        if isinstance(msg, str):
            st.chat_message(role).markdown(msg)
        else:
            st.chat_message(role).plotly_chart(msg)

def back():
    if st.session_state.chat_stage > 0:
        st.session_state.chat_stage -= 1
        if len(st.session_state.chat_history) >= 2:
            st.session_state.chat_history = st.session_state.chat_history[:-2]
        st.rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.chat_stage = 0
    st.session_state.chat_history = []
    st.session_state.welcome_shown = False
    st.rerun()
