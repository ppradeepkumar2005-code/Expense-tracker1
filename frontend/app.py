import streamlit as st

st.set_page_config(page_title="Expense Tracker", layout="wide")

# ================= API CONFIG =================
API_URL = "https://expense-trackerproject-7.onrender.com"
# ---------------- CSS STYLE ----------------
st.markdown("""
<style>
.main-title {
    font-size: 52px;
    font-weight: bold;
    text-align: center;
    color: #2E86C1;
}

.sub-text {
    font-size: 18px;
    text-align: center;
    color: gray;
}

.section-title {
    font-size: 28px;
    font-weight: bold;
    margin-top: 10px;
    color: blue;
    text-align: center;
}

.card {
    background: linear-gradient(135deg, #ffffff, #e8f0fe);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 4px 15px rgba(0,0,0,0.1);
    text-align: center;
    height: 170px;
    color: black;
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">💰 Expense Tracker App</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Track expenses, income & savings smartly</div>', unsafe_allow_html=True)

st.write("")

# ---------------- FEATURES ----------------
st.markdown('<div class="section-title">📌 Features</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>💸 Expense Management</h3>
        <p>✔ Add Expenses<br>✔ Edit Expenses<br>✔ Delete Expenses</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>💰 Income Tracking</h3>
        <p>✔ Add Income<br>✔ View Income<br>✔ Savings Calculation</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>📊 Reports</h3>
        <p>✔ Dashboard<br>✔ Charts<br>✔ PDF Reports</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------- BUTTONS ----------------
col4, col5 = st.columns(2)

with col4:
    if st.button("🔐 Login"):
        st.switch_page("pages/1_Login.py")

with col5:
    if st.button("📝 Register"):
        st.switch_page("pages/0_Register.py")

# ---------------- BACKEND CHECK ----------------
import requests

try:
    r = requests.get(f"{API_URL}/docs")
    st.success("✅ Backend Connected")
except:
    st.error("❌ Cannot connect to backend. Start FastAPI server first.")

# ---------------- FOOTER ----------------
st.markdown('<div class="footer">Made with ❤️ using Streamlit</div>', unsafe_allow_html=True)