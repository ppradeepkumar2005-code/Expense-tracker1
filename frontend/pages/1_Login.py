import streamlit as st
import requests

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

# If already logged in
if "token" in st.session_state:
    st.switch_page("pages/1_Dashboard.py")

st.title("🔐 Expense Tracker Login")

st.markdown("Login to continue")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login", use_container_width=True):

    if not username or not password:

        st.warning("Please fill all fields")

    else:

        try:

            response = requests.post(
                API_URL = "https://expense-trackerproject-7.onrender.com",
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

                try:
                    error_data = response.json()
                    st.error(
                        error_data.get(
                            "detail",
                            "Invalid Username or Password"
                        )
                    )
                except:
                    st.error("Invalid Username or Password")

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to backend. Start FastAPI server first."
            )

        except Exception as e:

            st.error(str(e))

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    if st.button(
        "📝 Create New Account",
        use_container_width=True
    ):
        st.switch_page("pages/0_Register.py")