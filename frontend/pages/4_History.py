import streamlit as st
import requests
import pandas as pd
from datetime import date

# ---------------- AUTH CHECK ----------------
if "token" not in st.session_state:
    st.warning("Please login first")
    st.switch_page("pages/1_Login.py")

st.set_page_config(page_title="Expense History", layout="wide")
st.title("📜 Transaction History")

API_URL = "http://localhost:8000"

headers = {
    "Authorization": f"Bearer {st.session_state['token']}"
}

# ---------------- FETCH EXPENSES ----------------
def get_expenses():
    res = requests.get(f"{API_URL}/expenses", headers=headers)
    if res.status_code == 200:
        return res.json()
    return []

# ---------------- DELETE ----------------
def delete_expense(expense_id):
    res = requests.delete(f"{API_URL}/expenses/{expense_id}", headers=headers)
    return res.status_code == 200

# ---------------- UPDATE ----------------
def update_expense(expense_id, data):
    res = requests.put(f"{API_URL}/expenses/{expense_id}", json=data, headers=headers)
    return res.status_code == 200


expenses = get_expenses()

if not expenses:
    st.info("No transactions found")
    st.stop()

df = pd.DataFrame(expenses)

# ---------------- DATE CONVERSION ----------------
df["date"] = pd.to_datetime(df["date"]).dt.date

# ---------------- FILTER UI ----------------
st.subheader("🔎 Filters")

col1, col2, col3 = st.columns(3)

with col1:
    start_date = st.date_input("Start Date", value=df["date"].min())

with col2:
    end_date = st.date_input("End Date", value=df["date"].max())

with col3:
    categories = ["All"] + sorted(df["category"].unique())
    selected_category = st.selectbox("Category", categories)

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df["date"] >= start_date) &
    (df["date"] <= end_date)
]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

st.divider()

# ---------------- TABLE HEADER ----------------
st.subheader("📋 Transactions")

# ---------------- EDIT STATE ----------------
if "edit_id" not in st.session_state:
    st.session_state["edit_id"] = None

# ---------------- DISPLAY ROWS ----------------
for _, row in filtered_df.iterrows():
    with st.container():
        c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 3, 2])

        c1.write(row["date"])
        c2.write(row["category"])
        c3.write(f"₹ {row['amount']}")
        c4.write(row.get("note", ""))

        # ---------------- EDIT ----------------
        if c5.button("✏️ Edit", key=f"edit_{row['id']}"):
            st.session_state["edit_id"] = row["id"]
            st.session_state["edit_data"] = row.to_dict()

        # ---------------- DELETE ----------------
        if c5.button("🗑️ Delete", key=f"delete_{row['id']}"):
            if delete_expense(row["id"]):
                st.success("Deleted successfully")
                st.rerun()
            else:
                st.error("Delete failed")

st.divider()

# ---------------- EDIT FORM ----------------
if st.session_state["edit_id"]:
    st.subheader("✏️ Edit Transaction")

    data = st.session_state["edit_data"]

    with st.form("edit_form"):
        amount = st.number_input("Amount", value=float(data["amount"]))
        category = st.text_input("Category", value=data["category"])
        date_val = st.date_input("Date", value=pd.to_datetime(data["date"]))
        note = st.text_area("Note", value=data.get("note", ""))

        submit = st.form_submit_button("Update")

        if submit:
            payload = {
                "amount": amount,
                "category": category,
                "date": str(date_val),
                "note": note
            }

            if update_expense(data["id"], payload):
                st.success("Updated successfully")
                st.session_state["edit_id"] = None
                st.session_state.pop("edit_data", None)
                st.rerun()
            else:
                st.error("Update failed")