import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- AUTH CHECK ----------------
if "token" not in st.session_state:
    st.warning("Please login first")
    st.switch_page("pages/1_Login.py")

st.title("📊 Expense Dashboard")

# ---------------- BACKEND URL ----------------
API_URL = "https://expense-trackerproject-7.onrender.com"

headers = {
    "Authorization": f"Bearer {st.session_state.get('token', '')}"
}

# ---------------- SAFE FETCH ----------------
def fetch(url):
    try:
        res = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        if res.status_code == 200:
            return res.json()

        return []

    except Exception:
        return []

# ---------------- GET DATA ----------------
expenses = fetch(f"{API_URL}/expenses")
income = fetch(f"{API_URL}/income")

# ---------------- DATAFRAME ----------------
df_exp = pd.DataFrame(expenses)
df_inc = pd.DataFrame(income)

# ---------------- DATE FORMAT ----------------
if not df_exp.empty and "date" in df_exp.columns:
    df_exp["date"] = pd.to_datetime(df_exp["date"])

if not df_inc.empty and "date" in df_inc.columns:
    df_inc["date"] = pd.to_datetime(df_inc["date"])

# ---------------- SUMMARY ----------------
st.subheader("📌 Summary")

total_expense = (
    df_exp["amount"].sum()
    if not df_exp.empty and "amount" in df_exp.columns
    else 0
)

total_income = (
    df_inc["amount"].sum()
    if not df_inc.empty and "amount" in df_inc.columns
    else 0
)

savings = total_income - total_expense

c1, c2, c3 = st.columns(3)

c1.metric("💰 Income", f"₹ {total_income}")
c2.metric("💸 Expense", f"₹ {total_expense}")
c3.metric("📈 Savings", f"₹ {savings}")

# ---------------- PIE CHART ----------------
st.subheader("🍕 Expense by Category")

if not df_exp.empty and "category" in df_exp.columns:

    fig = px.pie(
        df_exp,
        names="category",
        values="amount"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("No expense data available")

# ---------------- TRANSACTIONS ----------------
st.subheader("📋 Expenses")

if not df_exp.empty:
    st.dataframe(df_exp, use_container_width=True)
else:
    st.info("No expenses found")

st.subheader("💰 Income")

if not df_inc.empty:
    st.dataframe(df_inc, use_container_width=True)
else:
    st.info("No income found")