import streamlit as st

st.set_page_config(page_title="Expense Tracker", layout="wide")

# ================= API CONFIG =================
from utils.config import API_URL
st.markdown("""
<style>



/* Main Title */
.main-title {
    font-size: 55px;
    font-weight: 800;
    text-align: center;
    color: #1E3A8A;
    margin-bottom: 10px;
}

/* Subtitle */
.sub-text {
    font-size: 20px;
    text-align: center;
    color: #555;
    margin-bottom: 30px;
}

/* Section Title */
.section-title {
    font-size: 32px;
    font-weight: bold;
    text-align: center;
    color: #2563EB;
    margin-bottom: 25px;
}

/* Equal Size Cards */
.card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    height: 250px;   /* Same height for all cards */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.10);
    transition: all 0.3s ease;
    text-align: center;
}

.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 12px 25px rgba(37,99,235,0.25);
}

.card h3 {
    color: #2563EB;
    margin-bottom: 15px;
    font-size: 24px;
}

.card p {
    color: #444;
    font-size: 17px;
    line-height: 1.8;
}

/* Buttons */
div.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 50px;
    color: #777;
    font-size: 15px;
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


# ---------------- FOOTER ----------------
st.markdown('<div class="footer">Made with ❤️ using Streamlit</div>', unsafe_allow_html=True)