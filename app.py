import streamlit as st
import json
import os
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Burak GPT Admin",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOGIN ----------------
ADMIN_EMAIL = "burakerenkisapro1122@gmail.com"
ADMIN_PASSWORD = "burki4509"

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Admin Girişi")

    email = st.text_input("Email")
    password = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("❌ Yetkisiz giriş")

    st.stop()

# ---------------- DATA FILE ----------------
DATA_FILE = "admin_stats.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({
            "total_visits": 0,
            "image_requests": 0,
            "chat_requests": 0,
            "last_visit": None
        }, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

stats = load_data()

# ---------------- PANEL ----------------
st.title("📊 Burak GPT Admin Panel")

col1, col2, col3 = st.columns(3)

col1.metric("👥 Toplam Ziyaret", stats["total_visits"])
col2.metric("🎨 Görsel İstek", stats["image_requests"])
col3.metric("💬 Sohbet İstek", stats["chat_requests"])

st.divider()

st.subheader("🕒 Son Ziyaret")
st.write(stats["last_visit"] or "Henüz yok")

if st.button("🔄 Yenile"):
    st.rerun()

st.divider()

if st.button("🧹 Sayaçları Sıfırla"):
    stats = {
        "total_visits": 0,
        "image_requests": 0,
        "chat_requests": 0,
        "last_visit": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_data(stats)
    st.success("✅ Sıfırlandı")
