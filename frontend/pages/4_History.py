import streamlit as st
import requests
import pandas as pd

# ---------------- AUTH CHECK ----------------
if "token" not in st.session_state:
    st.warning("Please login first")
    st.switch_page("pages/1_Login.py")

st.set_page_config(page_title="Expense History", layout="wide")
st.title("📜 Transaction History")

# Render Backend URL
API_URL = "https://expense-trackerproject-7.onrender.com"

headers = {
    "Authorization": f"Bearer {st.session_state['token']}"
}

# ---------------- FETCH EXPENSES ----------------
def get_expenses():
    try:
        res = requests.get(
            f"{API_URL}/expenses",
            headers=headers,
            timeout=15
        )

        if res.status_code == 200:
            return res.json()

        st.error(f"API Error: {res.status_code}")
        return []

    except Exception as e:
        st.error(f"Connection Error: {e}")
        return []

# ---------------- DELETE ----------------
def delete_expense(expense_id):
    try:
        res = requests.delete(
            f"{API_URL}/expenses/{expense_id}",
            headers=headers
        )
        return res.status_code == 200
    except:
        return False

# ---------------- UPDATE ----------------
def update_expense(expense_id, data):
    try:
        res = requests.put(
            f"{API_URL}/expenses/{expense_id}",
            json=data,
            headers=headers
        )
        return res.status_code == 200
    except:
        return False

expenses = get_expenses()

if not expenses:
    st.info("No transactions found")
    st.stop()

df = pd.DataFrame(expenses)

st.dataframe(df, use_container_width=True)