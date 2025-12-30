import streamlit as st
import json
import os
from datetime import datetime

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Admin Panel", layout="wide")
st.title("🛠️ Yönetim Paneli")

# ===============================
# DATA FILE
# ===============================
USER_FILE = "users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({"users": {}}, f, indent=2)

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ===============================
# PERMISSIONS
# ===============================
ADMINS = [
"burakerenkisapro1122@gmail.com"
]

def is_admin(username):
    return username.lower() in [a.lower() for a in ADMINS]

# ===============================
# SESSION
# ===============================
if "admin" not in st.session_state:
    st.session_state.admin = None

# ===============================
# LOGIN
# ===============================
if st.session_state.admin is None:
    st.subheader("🔐 Admin Girişi")
    admin_name = st.text_input("Admin kullanıcı adı")

    if st.button("Giriş"):
        if is_admin(admin_name):
            st.session_state.admin = admin_name
            st.success("✅ Giriş başarılı")
            st.rerun()
        else:
            st.error("⛔ Yetkisiz erişim")

    st.stop()

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.write(f"👑 **Admin:** {st.session_state.admin}")
    if st.button("🚪 Çıkış Yap"):
        st.session_state.admin = None
        st.rerun()

# ===============================
# USER LIST
# ===============================
data = load_users()
users = data.get("users", {})

st.subheader("👥 Kullanıcılar")

if not users:
    st.info("Henüz kullanıcı yok")
else:
    for uid, user in users.items():
        col1, col2, col3 = st.columns([4, 2, 2])

        # STATUS
        if user.get("banned"):
            status = "🚫 Banlı"
        elif not user.get("active", True):
            status = "❌ Kapalı"
        else:
            status = "🟢 Aktif"

        col1.write(f"👤 **{uid}**")
        col1.caption(status)

        # BAN
        if col2.button("🚫 Ban", key=f"ban_{uid}"):
            user["banned"] = True
            save_users(data)
            st.rerun()

        # CLOSE
        if col3.button("❌ Hesap Kapat", key=f"close_{uid}"):
            user["active"] = False
            save_users(data)
            st.rerun()
