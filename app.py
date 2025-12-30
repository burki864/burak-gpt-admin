import streamlit as st
import os

# ================== CONFIG ==================
ADMIN_EMAIL = "burakerenkisapro1122@gmail.com"
ADMIN_PASSWORD = "burki4509"

VISITOR_FILE = "visitors.txt"
CLICK_FILE = "clicks.txt"

# ================== HELPERS ==================
def read_count(file):
    if not os.path.exists(file):
        return 0
    with open(file, "r") as f:
        data = f.read().strip()
        return int(data) if data.isdigit() else 0

# ================== PAGE ==================
st.set_page_config(
    page_title="Burak GPT | Admin",
    page_icon="🔐",
    layout="centered"
)

# ================== SESSION ==================
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# ================== LOGIN SCREEN ==================
if not st.session_state.admin_logged:
    st.title("🔐 Yapımcı Girişi")
    st.caption("Bu sayfa yalnızca yetkili kişiye açıktır")

    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Şifre", type="password")

    if st.button("Giriş Yap"):
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            st.session_state.admin_logged = True
            st.success("✅ Giriş başarılı")
            st.rerun()
        else:
            st.error("❌ Email veya şifre yanlış")

    st.stop()  # 🚨 LOGIN OLMADAN AŞAĞISI ASLA ÇALIŞMAZ

# ================== ADMIN PANEL ==================
st.title("📊 Burak GPT – Yönetici Paneli")
st.caption("Canlı kullanım ve etkileşim verileri")

visitors = read_count(VISITOR_FILE)
clicks = read_count(CLICK_FILE)

col1, col2 = st.columns(2)
col1.metric("👥 Toplam Ziyaretçi", visitors)
col2.metric("🖱️ Toplam Tıklanma", clicks)

st.divider()

st.subheader("📈 Genel Aktivite Özeti")
st.bar_chart({
    "Ziyaretçiler": visitors,
    "Tıklanmalar": clicks
})

st.divider()

if st.button("🚪 Çıkış Yap"):
    st.session_state.admin_logged = False
    st.rerun()
