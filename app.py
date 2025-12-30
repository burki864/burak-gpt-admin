import streamlit as st
import json
import os
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Burak GPT | Admin Panel",
    page_icon="🛡️",
    layout="wide"
)

ADMIN_EMAIL = "burakerenkisapro1122@gmail.com"
ADMIN_PASSWORD = "burki4509"

USERS_FILE = "users.json"

# ---------------- HELPERS ----------------
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- AUTH ----------------
if "admin_auth" not in st.session_state:
    st.session_state.admin_auth = False

if not st.session_state.admin_auth:
    st.title("🔐 Admin Girişi")

    email = st.text_input("Email")
    password = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            st.session_state.admin_auth = True
            st.rerun()
        else:
            st.error("❌ Yetkisiz giriş")

    st.stop()

# ---------------- PANEL ----------------
st.title("🛡️ Kullanıcı Yönetim Paneli")

users = load_users()

if not users:
    st.info("Henüz kullanıcı yok")
    st.stop()

st.markdown("---")

for uid, data in users.items():
    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])

    with col1:
        st.markdown(f"### 👤 {uid}")
        st.caption(f"Ad: {data.get('name')}")
        st.caption(f"Oluşturulma: {data.get('created_at')}")

    with col2:
        status = "🟢 Aktif" if data["active"] else "⚫ Kapalı"
        st.markdown(status)

    with col3:
        ban = "🚫 Banned" if data["banned"] else "✅ Temiz"
        st.markdown(ban)

    with col4:
        if st.button("👁️ Görüntüle", key=f"view_{uid}"):
            st.info(json.dumps(data, indent=2, ensure_ascii=False))

    with col5:
        if st.button("🚫 Banla", key=f"ban_{uid}"):
            users[uid]["banned"] = True
            save_users(users)
            st.warning(f"{uid} banlandı")
            st.rerun()

        if st.button("❌ Hesabı Kapat", key=f"close_{uid}"):
            users[uid]["active"] = False
            save_users(users)
            st.error(f"{uid} hesabı kapatıldı")
            st.rerun()

    st.markdown("---")
