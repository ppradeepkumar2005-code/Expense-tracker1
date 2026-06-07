import streamlit as st

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# ---------------- LOGIN CHECK ----------------
if "token" not in st.session_state:
    st.switch_page("pages/1_Login.py")

st.sidebar.title("💰 Expense Tracker")

menu = st.sidebar.selectbox(
    "Navigate",
    [
        "Dashboard",
        "Add Expense",
        "Add Income",
        "History"
    ]
)

# ---------------- LOGOUT ----------------
if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.switch_page("pages/1_Login.py")

# ---------------- PAGE ROUTING ----------------

if menu == "Dashboard":
    st.switch_page("pages/1_Dashboard.py")

elif menu == "Add Expense":
    st.switch_page("pages/2_Add_Expense.py")

elif menu == "Add Income":
    st.switch_page("pages/3_Add_Income.py")

elif menu == "History":
    st.switch_page("pages/4_History.py")