import streamlit as st
from datetime import datetime, timedelta
from supabase import create_client

# ================= PAGE =================
st.set_page_config(
    page_title="Admin Panel",
    page_icon="🛠️",
    layout="wide"
)

# ================= SUPABASE =================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
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

# ================= HELPERS =================
def is_online(last_seen):
    if not last_seen:
        return False
    return datetime.utcnow() - last_seen < timedelta(seconds=90)

# ================= LOAD USERS =================
res = supabase.table("users").select("*").execute()
users = res.data or []

st.title("🛠️ Admin Panel")

if not users:
    st.info("Henüz kayıtlı kullanıcı yok")
    st.stop()

# ================= USER LIST =================
st.markdown("## 👥 Kullanıcılar")

for u in users:
    online = is_online(u["last_seen"])
    status = "🟢 Online" if online else "🔴 Offline"
    banned = "🚫 Banlı" if u["banned"] else "✅ Aktif"
    deleted = "🧹 Silinmiş" if u["deleted"] else ""

    st.write(f"**{u['username']}** → {status} | {banned} {deleted}")

st.markdown("---")

# ================= USER ACTION =================
usernames = [u["username"] for u in users]
selected = st.selectbox("Kullanıcı Seç", usernames)

user = next(u for u in users if u["username"] == selected)

st.markdown("### Kullanıcı Bilgisi")
st.json(user)

c1, c2, c3, c4 = st.columns(4)

if c1.button("🚫 Banla"):
    supabase.table("users").update({"banned": True}).eq("id", user["id"]).execute()
    st.success("Kullanıcı banlandı")
    st.rerun()

if c2.button("✅ Unban"):
    supabase.table("users").update({"banned": False}).eq("id", user["id"]).execute()
    st.success("Ban kaldırıldı")
    st.rerun()

if c3.button("🧹 Soft Delete"):
    supabase.table("users").update({"deleted": True}).eq("id", user["id"]).execute()
    st.success("Hesap devre dışı bırakıldı")
    st.rerun()

if c4.button("♻️ Geri Aç"):
    supabase.table("users").update({"deleted": False}).eq("id", user["id"]).execute()
    st.success("Hesap geri açıldı")
    st.rerun()

# ================= BACK =================
st.markdown(
    """
    <a href="https://burak-gpt.streamlit.app">
        ⬅️ GPT’ye Dön
    </a>
    """,
    unsafe_allow_html=True
)
