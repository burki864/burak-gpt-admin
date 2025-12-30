import streamlit as st
from utils import load_users, save_users
from permissions import is_admin

st.set_page_config(
    page_title="Burak GPT | Admin Panel",
    page_icon="🛠️",
    layout="wide"
)

# --- LOGIN ---
if "admin" not in st.session_state:
    st.session_state.admin = None

if st.session_state.admin is None:
    st.title("🔐 Admin Girişi")
    admin_name = st.text_input("Admin kullanıcı adı")

    if st.button("Giriş"):
        if is_admin(admin_name):
            st.session_state.admin = admin_name
            st.rerun()
        else:
            st.error("⛔ Yetkisiz erişim")
    st.stop()

# --- PANEL ---
st.sidebar.success(f"👑 Admin: {st.session_state.admin}")
if st.sidebar.button("🚪 Çıkış Yap"):
    st.session_state.admin = None
    st.rerun()

st.title("🛠️ Burak GPT Yönetim Paneli")

data = load_users()
users = data.get("users", {})

if not users:
    st.info("Henüz kullanıcı yok")
    st.stop()

for uid, user in users.items():
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([3,2,2,2])

        col1.markdown(
            f"""
            **👤 {uid}**  
            İsim: `{user['name']}`  
            Oluşturulma: `{user['created_at']}`
            """
        )

        status = "🟢 Aktif" if user["active"] else "⚪ Kapalı"
        ban = "🚫 Banned" if user["banned"] else "✅ Temiz"

        col2.write(status)
        col2.write(ban)

        if col3.button("🚫 Ban", key=f"ban_{uid}"):
            user["banned"] = True
            save_users(data)
            st.rerun()

        if col4.button("❌ Hesap Kapat", key=f"close_{uid}"):
            user["active"] = False
            save_users(data)
            st.rerun()
