import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG (MUST BE FIRST) ----------------
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

API_URL = "http://127.0.0.1:8000"

headers = {
    "Authorization": f"Bearer {st.session_state.get('token', '')}"
}

# ---------------- SAFE FETCH FUNCTION ----------------
def fetch(url):
    try:
        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"API Error {res.status_code}: {res.text}")
            return []

    except requests.exceptions.ConnectionError:
        st.error("❌ Backend not running")
        return []

    except Exception as e:
        st.error(f"API Error: {e}")
        return []

# ---------------- GET DATA ----------------
expenses = fetch(f"{API_URL}/expenses")
income = fetch(f"{API_URL}/income")

# ---------------- DATAFRAME ----------------
df_exp = pd.DataFrame(expenses)
df_inc = pd.DataFrame(income)

# ---------------- DATE CLEAN ----------------
if not df_exp.empty and "date" in df_exp.columns:
    df_exp["date"] = pd.to_datetime(df_exp["date"])

if not df_inc.empty and "date" in df_inc.columns:
    df_inc["date"] = pd.to_datetime(df_inc["date"])

# ---------------- MONTH LIST ----------------
st.sidebar.subheader("📅 Filter")

if not df_exp.empty and "date" in df_exp.columns:
    all_months = sorted(df_exp["date"].dt.to_period("M").astype(str).unique())
else:
    all_months = []

selected_month = st.sidebar.selectbox("Select Month", all_months) if all_months else None

# ---------------- FILTER DATA ----------------
if selected_month and not df_exp.empty:
    df_exp = df_exp[df_exp["date"].dt.to_period("M").astype(str) == selected_month]

if selected_month and not df_inc.empty:
    df_inc = df_inc[df_inc["date"].dt.to_period("M").astype(str) == selected_month]

# ---------------- SUMMARY ----------------
st.subheader("📌 Monthly Summary")

total_expense = df_exp["amount"].sum() if not df_exp.empty else 0
total_income = df_inc["amount"].sum() if not df_inc.empty else 0
net_savings = total_income - total_expense

col1, col2, col3 = st.columns(3)

col1.metric("💰 Income", f"₹ {total_income}")
col2.metric("💸 Expense", f"₹ {total_expense}")
col3.metric("📈 Savings", f"₹ {net_savings}")

# ---------------- CATEGORY PIE ----------------
st.subheader("🍕 Expense by Category")

if not df_exp.empty and "category" in df_exp.columns:
    fig1 = px.pie(
        df_exp,
        names="category",
        values="amount",
        title="Expense by Category"
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No category data")

# ---------------- INCOME VS EXPENSE ----------------
st.subheader("📊 Income vs Expense Over Time")

if not df_exp.empty or not df_inc.empty:

    exp_time = df_exp.groupby("date")["amount"].sum().reset_index() if not df_exp.empty else pd.DataFrame(columns=["date", "amount"])
    inc_time = df_inc.groupby("date")["amount"].sum().reset_index() if not df_inc.empty else pd.DataFrame(columns=["date", "amount"])

    exp_time["type"] = "Expense"
    inc_time["type"] = "Income"

    df_time = pd.concat([exp_time, inc_time])

    fig2 = px.bar(
        df_time,
        x="date",
        y="amount",
        color="type",
        barmode="group"
    )

    st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("No data for chart")

# ---------------- TABLE ----------------
st.subheader("📋 Transactions")

if not df_exp.empty:
    st.write("### Expenses")
    st.dataframe(df_exp, use_container_width=True)

if not df_inc.empty:
    st.write("### Income")
    st.dataframe(df_inc, use_container_width=True)