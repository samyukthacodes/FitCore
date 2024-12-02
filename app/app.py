import streamlit as st

from utils.signin import show_signin_page
from pages.signup import show_signup_page


def main():
    
    st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    )

    
    show_signin_page()

if __name__ == "__main__":
    if 'authenticated' not in st.session_state:
        st.session_state["authenticated"] = False
    main()