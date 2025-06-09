import streamlit as st
from .database import register_user, validate_user
import boto3


def auth_ui():
    st.title("🔐 Login or Register")

    mode = st.radio("Choose mode", ["Login", "Register"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Register":
        if st.button("Register"):
            if register_user(email, password):
                st.success("Registered successfully. You can now log in.")
            else:
                st.error("Email already registered.")
    else:
        if st.button("Login"):
            if validate_user(email, password):
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials.")


def fetch_deep_seek_api_key():
    ssm = boto3.client('ssm', region_name='us-east-2')
    response = ssm.get_parameter(Name='deep_seek_api_key', WithDecryption=True)
    return response['Parameter']['Value']
