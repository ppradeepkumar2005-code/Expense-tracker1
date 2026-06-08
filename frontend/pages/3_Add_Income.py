import streamlit as st
import requests
from datetime import date

# ---------------- AUTH CHECK ----------------
if "token" not in st.session_state:
    st.warning("Please login first")
    st.switch_page("pages/1_Login.py")

st.set_page_config(page_title="Add Income", layout="centered")
st.title("💰 Add Income")

# 🔥 CHANGE THIS (IMPORTANT)
API_URL = "https://your-backend-name.onrender.com"  
# OR for local: "http://127.0.0.1:8000"

headers = {
    "Authorization": f"Bearer {st.session_state['token']}"
}

# ---------------- SUBMIT INCOME ----------------
def add_income(payload):
    try:
        res = requests.post(
            f"{API_URL}/income",
            json=payload,
            headers=headers,
            timeout=10
        )

        # Debug (optional)
        # st.write(res.status_code, res.text)

        return res.status_code == 200

    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {e}")
        return False

# ---------------- FORM ----------------
with st.form("income_form"):
    amount = st.number_input("Amount", min_value=0.0, step=100.0)
    source = st.text_input("Source (Salary / Freelance / Other)")
    income_date = st.date_input("Date", value=date.today())

    submit = st.form_submit_button("Add Income")

    if submit:
        if amount <= 0:
            st.error("Amount must be greater than 0")
        elif not source:
            st.error("Please enter income source")
        else:
            payload = {
                "amount": float(amount),
                "source": source,
                "date": str(income_date)
            }

            if add_income(payload):
                st.success("Income added successfully 🎉")
                st.rerun()
            else:
                st.error("Failed to add income")