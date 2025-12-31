import streamlit as st
import json, os
from datetime import datetime, timedelta

# ================= PAGE =================
st.set_page_config(
    page_title="Admin Panel",
    page_icon="🛠️",
    layout="wide"
)

# ================= AUTH =================
if "admin" not in st.session_state:
    st.session_state.admin = False

if not st.session_state.admin:
    st.title("🔐 Admin Girişi")
    key = st.text_input("Admin Key", type="password")

    if st.button("Giriş"):
        if key == st.secrets["ADMIN_KEY"]:
            st.session_state.admin = True
            st.rerun()
        else:
            st.error("❌ Yetkisiz erişim")

    st.stop()

# ================= USERS IO =================
USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

users = load_users()

# ================= ONLINE CHECK =================
def is_online(last_seen):
    if not last_seen:
        return False
    try:
        t = datetime.fromisoformat(last_seen)
        return datetime.utcnow() - t < timedelta(seconds=90)
    except:
        return False

# ================= UI =================
st.title("🛠️ Admin Panel")

if not users:
    st.info("Henüz kayıtlı kullanıcı yok")
    st.stop()

# ---------- USER LIST ----------
st.markdown("## 👥 Kullanıcılar")

for name, info in users.items():
    online = is_online(info.get("last_seen"))
    status = "🟢 Online" if online else "🔴 Offline"
    banned = "🚫 Banlı" if info.get("banned") else "✅ Aktif"
    deleted = "🧹 Silinmiş" if info.get("deleted") else ""

    st.write(f"**{name}** → {status} | {banned} {deleted}")

st.markdown("---")

# ---------- USER ACTIONS ----------
user = st.selectbox("Kullanıcı Seç", list(users.keys()))
info = users[user]

st.markdown("### Kullanıcı Bilgisi")
st.json(info)

c1, c2, c3, c4 = st.columns(4)

if c1.button("🚫 Banla"):
    users[user]["banned"] = True
    save_users(users)
    st.success("Kullanıcı banlandı")
    st.rerun()

if c2.button("✅ Unban"):
    users[user]["banned"] = False
    save_users(users)
    st.success("Ban kaldırıldı")
    st.rerun()

if c3.button("🧹 Soft Delete"):
    users[user]["deleted"] = True
    save_users(users)
    st.success("Hesap devre dışı bırakıldı")
    st.rerun()

if c4.button("♻️ Geri Aç"):
    users[user]["deleted"] = False
    save_users(users)
    st.success("Hesap geri açıldı")
    st.rerun()

st.markdown("---")

# ---------- BACK ----------
st.markdown(
    """
    <a href="https://burak-gpt.streamlit.app">
        ⬅️ GPT’ye Dön
    </a>
    """,
    unsafe_allow_html=True
)
