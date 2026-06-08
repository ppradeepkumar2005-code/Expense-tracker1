import streamlit as st
import requests

API_URL = "https://expense-trackerproject-7.onrender.com"

st.set_page_config(
    page_title="Register",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Create Account")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Register"):

    if not username or not password:
        st.warning("Please fill all fields")

    else:
        try:
            response = requests.post(
                f"{API_URL}/auth/register",   # ✅ FIXED HERE
                json={
                    "username": username,
                    "password": password
                }
            )

            if response.status_code in [200, 201]:
                st.success("Registration Successful ✅")
                st.switch_page("pages/1_Login.py")

            else:
                st.error(response.text)

        except Exception as e:
            st.error(str(e))

if st.button("Already have an account? Login"):
    st.switch_page("pages/1_Login.py")