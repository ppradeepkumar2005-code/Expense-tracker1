import streamlit as st
import requests
import pandas as pd
from datetime import date

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Add Expense",
    page_icon="➕",
    layout="wide"
)

# ---------------- AUTH CHECK ----------------
if "token" not in st.session_state:
    st.warning("Please login first")
    st.switch_page("pages/1_Login.py")

st.title("➕ Add / Manage Expenses")

# ---------------- BACKEND URL ----------------
API_URL = "https://expense-trackerproject-7.onrender.com"

headers = {
    "Authorization": f"Bearer {st.session_state['token']}"
}

# ---------------- FETCH EXPENSES ----------------
def fetch_expenses():
    try:
        res = requests.get(
            f"{API_URL}/expenses",
            headers=headers,
            timeout=20
        )

        if res.status_code == 200:
            return res.json()

        st.error(f"API Error: {res.status_code}")
        return []

    except Exception as e:
        st.error(f"Connection Error: {e}")
        return []

# ---------------- ADD EXPENSE ----------------
st.subheader("➕ Add Expense")

with st.form("add_form"):

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        format="%.2f"
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Bills",
            "Shopping",
            "Other"
        ]
    )

    expense_date = st.date_input(
        "Date",
        value=date.today()
    )

    note = st.text_area("Note")

    submit = st.form_submit_button("Add Expense")

if submit:

    payload = {
        "amount": float(amount),
        "category": category,
        "date": str(expense_date),
        "note": note
    }

    try:

        res = requests.post(
            f"{API_URL}/expenses",
            json=payload,
            headers=headers,
            timeout=20
        )

        if res.status_code in [200, 201]:
            st.success("Expense Added Successfully ✅")
            st.rerun()

        else:
            st.error(res.text)

    except Exception as e:
        st.error(str(e))

# ---------------- SHOW EXPENSES ----------------
st.divider()
st.subheader("📋 All Expenses")

data = fetch_expenses()

if data:

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True
    )

else:
    st.info("No expenses found")