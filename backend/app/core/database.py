import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "https://expense-trackerproject-7.onrender.com"

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Expense Dashboard")

headers = {}

if "token" in st.session_state:
    headers = {
        "Authorization": f"Bearer {st.session_state['token']}"
    }

# ---------------- BACKEND CHECK ----------------
try:
    health = requests.get(f"{API_URL}/health")

    if health.status_code == 200:
        st.success("✅ Backend Connected")
    else:
        st.error("❌ Backend not running")

except Exception as e:
    st.error("❌ Backend not running")
    st.stop()

# ---------------- SUMMARY ----------------
try:
    summary = requests.get(
        f"{API_URL}/summary",
        headers=headers
    )

    if summary.status_code == 200:
        data = summary.json()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("💰 Income", f"₹{data.get('income',0)}")

        with col2:
            st.metric("💸 Expense", f"₹{data.get('expense',0)}")

        with col3:
            st.metric("📈 Savings", f"₹{data.get('savings',0)}")

except Exception as e:
    st.error(str(e))

# ---------------- CATEGORY CHART ----------------
try:
    category = requests.get(
        f"{API_URL}/categories",
        headers=headers
    )

    if category.status_code == 200:

        cat_data = category.json()

        if len(cat_data) > 0:

            df = pd.DataFrame(cat_data)

            fig = px.pie(
                df,
                names="category",
                values="total",
                title="Expense By Category"
            )

            st.plotly_chart(fig, use_container_width=True)

except Exception:
    pass