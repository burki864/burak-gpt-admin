import streamlit as st
from permissions import check_admin
from utils import load_users, save_users

st.title("🔐 Admin Girişi")

email = st.text_input("Admin e-posta")
password = st.text_input("Şifre", type="password")

if st.button("Giriş"):
    if check_admin(email, password):
        st.session_state["admin"] = True
        st.success("✅ Giriş başarılı")
    else:
        st.error("⛔ Yetkisiz erişim")

if st.session_state.get("admin"):
    st.divider()
    st.header("🛠️ Yönetim Paneli")

    data = load_users()

    for uid, user in data["users"].items():
        col1, col2, col3 = st.columns([4,2,2])

        col1.write(f"👤 {uid} | {user['name']}")

    if col2.button("🚫 Ban", key=f"ban_{uid}"):
    user["banned"] = True
    save_users(data)
    st.rerun()

elif col3.button("❌ Hesap Kapat", key=f"close_{uid}"):
    user["active"] = False
    save_users(data)
    st.rerun()
