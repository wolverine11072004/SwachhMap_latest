import streamlit as st
from ui import show_home_page, show_login_page, show_signup_page, main_app
import os, time

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ''
    st.session_state.page = 'home'

def main():
    if st.session_state.page == 'home':
        show_home_page()
    elif st.session_state.page == 'login':
        show_login_page()
    elif st.session_state.page == 'signup':
        show_signup_page()
    elif st.session_state.page == 'app':
        main_app()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        st.error(f'An error occurred: {e}')
