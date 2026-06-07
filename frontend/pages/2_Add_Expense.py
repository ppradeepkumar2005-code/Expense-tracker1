import streamlit as st
import requests
import pandas as pd
from datetime import date

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Add Expense", page_icon="➕", layout="wide")

# ---------------- AUTH CHECK ----------------
if "token" not in st.session_state:
    st.warning("Please login first")
    st.switch_page("pages/1_Login.py")

st.title("➕ Add / Manage Expenses")

API_URL = "http://127.0.0.1:8000"

headers = {
    "Authorization": f"Bearer {st.session_state['token']}"
}

# ---------------- API CALL ----------------
def fetch_expenses():
    res = requests.get(f"{API_URL}/expenses", headers=headers)
    if res.status_code == 200:
        return res.json()
    return []

# ---------------- ADD EXPENSE ----------------
st.subheader("➕ Add Expense")

with st.form("add_form"):

    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Transport", "Bills", "Shopping", "Other"])
    expense_date = st.date_input("Date", value=date.today())
    note = st.text_area("Note")

    submit = st.form_submit_button("Add Expense")

if submit:

    payload = {
        "amount": float(amount),
        "category": category,
        "date": str(expense_date),
        "note": note
    }

    res = requests.post(f"{API_URL}/expenses", json=payload, headers=headers)

    if res.status_code in [200, 201]:
        st.success("Expense Added ✅")
        st.rerun()
    else:
        st.error(res.text)

# ---------------- SHOW EXPENSES ----------------
st.divider()
st.subheader("📋 All Expenses")

data = fetch_expenses()

if data:

    df = pd.DataFrame(data)

    # ---------------- EDIT ----------------
    for i, row in df.iterrows():

        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])

        with col1:
            st.write(row["amount"])

        with col2:
            st.write(row["category"])

        with col3:
            st.write(row["date"])

        with col4:

            if st.button("✏️ Edit", key=f"edit_{row['id']}"):

                new_amount = st.number_input(
                    "New Amount",
                    value=float(row["amount"]),
                    key=f"amt_{row['id']}"
                )

                new_category = st.selectbox(
                    "New Category",
                    ["Food", "Transport", "Bills", "Shopping", "Other"],
                    index=["Food", "Transport", "Bills", "Shopping", "Other"].index(row["category"]),
                    key=f"cat_{row['id']}"
                )

                if st.button("Save", key=f"save_{row['id']}"):

                    update_payload = {
                        "amount": new_amount,
                        "category": new_category,
                        "date": row["date"],
                        "note": row.get("note", "")
                    }

                    res = requests.put(
                        f"{API_URL}/expenses/{row['id']}",
                        json=update_payload,
                        headers=headers
                    )

                    if res.status_code == 200:
                        st.success("Updated ✅")
                        st.rerun()
                    else:
                        st.error(res.text)

        with col5:

            if st.button("🗑️ Delete", key=f"del_{row['id']}"):

                res = requests.delete(
                    f"{API_URL}/expenses/{row['id']}",
                    headers=headers
                )

                if res.status_code == 204:
                    st.success("Deleted ✅")
                    st.rerun()
                else:
                    st.error(res.text)

else:
    st.info("No expenses found")