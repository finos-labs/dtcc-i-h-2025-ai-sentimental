import streamlit as st
from .ai import ask_langchain_db, run_rag_query

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

def get_response(prompt, model_choice):
    if model_choice == "Database":
        return ask_langchain_db(prompt)
    elif model_choice == "Web":
        return run_rag_query(prompt)
    return "❌ Invalid model selected."

def chat_ui():
    st.title("🤖 FINSEEK CHATBOT")

    # Dropdown to choose model
    model_choice = st.sidebar.selectbox("Model:", ["Database", "Web"])

    # Chat input
    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.current_chat.append({
            "role": "user", 
            "content": user_input,
            "model": model_choice
        })

        response = get_response(user_input, model_choice)

        st.session_state.current_chat.append({
            "role": "bot", 
            "content": response,
            "model": model_choice
        })

    # Display messages
    for message in st.session_state.current_chat:
        with st.chat_message("user" if message["role"] == "user" else "assistant"):
            st.markdown(f"_{message.get('model', '🤖')}_: {message['content']}")
