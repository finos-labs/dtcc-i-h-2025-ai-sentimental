import streamlit as st
from .ai import ask_langchain_db

def get_response_from_deepseek(prompt):
    # Replace with actual DeepSeek API call logic
    res = ask_langchain_db(prompt)
    return f"{res}"

def init_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_chat' not in st.session_state:
        st.session_state.current_chat = []

def sidebar_ui():
    st.sidebar.title("💬 Chat History")

    if st.sidebar.button("➕ New Chat"):
        if st.session_state.current_chat:
            st.session_state.chat_history.append(st.session_state.current_chat.copy())
        st.session_state.current_chat = []

    for i, chat in enumerate(reversed(st.session_state.chat_history), 1):
        with st.sidebar.expander(f"Previous Chat #{len(st.session_state.chat_history) - i + 1}"):
            for msg in chat:
                st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

def chat_ui():
    st.title("🤖 FINSEEK CHATBOT")

    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.current_chat.append({"role": "user", "content": user_input})
        response = get_response_from_deepseek(user_input)
        st.session_state.current_chat.append({"role": "bot", "content": response})

    for message in st.session_state.current_chat:
        with st.chat_message("user" if message["role"] == "user" else "assistant"):
            st.markdown(message["content"])
