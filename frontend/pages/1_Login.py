import streamlit as st
import requests

API_URL = "https://expense-trackerproject-7.onrender.com"

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Expense Tracker Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    try:

        response = requests.post(
            f"{API_URL}/auth/auth/login",
            json={
                "username": username,
                "password": password
            }
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state["token"] = data["access_token"]

            st.success("Login Successful ✅")

            st.switch_page("pages/1_Dashboard.py")

        else:
            st.error(response.text)

    except Exception as e:
        st.error(str(e))