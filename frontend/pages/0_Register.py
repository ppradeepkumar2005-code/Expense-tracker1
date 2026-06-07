import streamlit as st
import requests

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
                "http://127.0.0.1:8000/auth/auth/register",
                json={
                    "username": username,
                    "password": password
                }
            )

            if response.status_code in [200, 201]:

                st.success("Registration Successful ✅")
                st.info("Redirecting to Login Page...")

                import time
                time.sleep(2)

                st.switch_page("pages/1_Login.py")

            else:

                try:
                    error_data = response.json()

                    if "already" in str(error_data).lower():
                        st.warning(
                            "You already have an account. Please login."
                        )

                        if st.button("Go to Login"):
                            st.switch_page("pages/1_Login.py")

                    else:
                        st.error(
                            error_data.get(
                                "detail",
                                f"Server Error ({response.status_code})"
                            )
                        )

                except Exception:
                    st.error(
                        f"Server Error ({response.status_code})"
                    )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to backend. Start FastAPI server first."
            )

        except Exception as e:

            st.error(str(e))

st.markdown("---")

if st.button("Already have an account? Login"):
    st.switch_page("pages/1_Login.py")