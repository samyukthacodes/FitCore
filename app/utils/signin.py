import streamlit as st
from utils.database import * 
from pages.viewnotes import *

def show_signin_page():
    st.title("Signin Page")
    if st.session_state["authenticated"] == False:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Sign In"):
            if authenticate_user(username, password):
                st.session_state["authenticated"] = True
                st.session_state['username'] = username
                st.success("Signed in successful!")
                
            else:
                st.session_state["authenticated"] = False
                st.error("Invalid username or password.")
    else:
        st.title("Welcome to FitCore")
            

if __name__ == "__main__":
    show_signin_page()
