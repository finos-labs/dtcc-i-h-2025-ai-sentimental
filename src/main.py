import streamlit as st
from finbot_mods.auth import auth_ui
from finbot_mods.chat_ui import init_session_state, sidebar_ui, chat_ui
from finbot_mods.database import init_db
import os

os.environ["AWS_REGION"] = "us-east-2"

# Initialize DB
init_db()

# Track authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Sidebar logout button (available only when logged in)
if st.session_state.authenticated:
    with st.sidebar:
        st.markdown(f"**Logged in as:** {st.session_state.get('user_email', 'unknown')}")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.session_state.current_chat = []
            st.session_state.chat_history = []
            st.rerun()

# Show chatbot or login screen
if st.session_state.authenticated:
    init_session_state()
    sidebar_ui()
    chat_ui()
else:
    auth_ui()
