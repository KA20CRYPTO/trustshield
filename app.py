import streamlit as st
from firebase_config import auth

st.title("TruthShield AI 🔐")

choice = st.selectbox("Login / Signup", ["Login", "Sign Up"])

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if choice == "Sign Up":
    if st.button("Create Account"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success("Account created! Please login.")
        except:
            st.error("Signup failed")

if choice == "Login":
    if st.button("Login"):
        try:
            auth.sign_in_with_email_and_password(email, password)
            st.success("Login successful!")
            st.session_state["user"] = email
        except:
            st.error("Login failed")
