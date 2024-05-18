import streamlit as st
with st.form("Login"):
    st.write("login")
    st.text_input("Username",placeholder="enter username or email")
    st.text_input("Password",placeholder="enter password",type="password")
    if st.form_submit_button("login"):
        st.switch_page("pages/mainapp.py")



