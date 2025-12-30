import streamlit as st
from utils import load_users, save_users
from permissions import is_admin

st.set_page_config(page_title="Admin Panel", layout="wide")
st.title("🛠️ Yönetim Paneli")

# --- Admin giriş ---
if "admin" not in st.session_state:
    st.session_state.admin = None

if not st.session_state.admin:
    admin_name = st.text_input("Admin kullanıcı adı")

    if st.button("Giriş"):
        if is_admin(admin_name):
            st.session_state.admin = admin_name
            st.rerun()
        else:
            st.error("⛔ Yetkisiz erişim")

    st.stop()

# --- Çıkış ---
with st.sidebar:
    st.write(f"👑 Admin: {st.session_state.admin}")
    if st.button("🚪 Çıkış Yap"):
        st.session_state.admin = None
        st.rerun()

# --- Kullanıcı listesi ---
data = load_users()

st.subheader("👥 Kullanıcılar")

for uid, user in data["users"].items():
    col1, col2, col3 = st.columns([4, 2, 2])

    status = "🟢 Aktif"
    if user.get("banned"):
        status = "🚫 Banlı"
    elif not user.get("active", True):
        status = "❌ Kapalı"

    col1.write(f"👤 {uid} | {user.get('name', '-')}")
    col1.caption(status)

    if col2.button("🚫 Ban", key=f"ban_{uid}"):
        user["banned"] = True
        save_users(data)
        st.rerun()

    if col3.button("❌ Hesap Kapat", key=f"close_{uid}"):
        user["active"] = False
        save_users(data)
        st.rerun()
