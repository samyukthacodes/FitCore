import streamlit as st
from utils.database import *

def show_signup_page():
    st.title("Signup Page")

    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")

    

    if st.button("Sign Up"):
        if add_user(username, password):
            st.success("Signup successful! You can now log in.")
        else:
            st.error("Username already exists.")

if __name__ == "__main__":
    show_signup_page()