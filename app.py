import streamlit as st
import json, os

st.set_page_config(page_title="Yönetim Paneli", layout="wide")

ADMINS = ["burakerenkisapro1122@gmail.com", "burak"]

USER_FILE = "users.json"

def load_users():
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------- ADMIN LOGIN ----------
if "admin" not in st.session_state:
    st.session_state.admin = None

if not st.session_state.admin:
    name = st.text_input("Admin kullanıcı adı")
    if st.button("Giriş"):
        if name in ADMINS:
            st.session_state.admin = name
            st.rerun()
        else:
            st.error("⛔ Yetkisiz")
    st.stop()

# ---------- PANEL ----------
st.title("🛠️ Yönetim Paneli")
data = load_users()

for uid, user in data["users"].items():
    col1, col2, col3 = st.columns([4,2,2])

    status = "🟢 Aktif"
    if user.get("banned"):
        status = "🚫 Banlı"
    elif not user.get("active"):
        status = "❌ Kapalı"

    col1.write(f"👤 {uid}")
    col1.caption(status)

    if col2.button("🚫 Ban", key=f"ban_{uid}"):
        user["banned"] = True
        save_users(data)
        st.rerun()

    if col3.button("❌ Kapat", key=f"close_{uid}"):
        user["active"] = False
        save_users(data)
        st.rerun()
