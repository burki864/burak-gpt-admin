import streamlit as st
import json
import os
from datetime import datetime

# ================== AYARLAR ==================
ADMIN_EMAIL = "burakerenkisapro1122@gmail.com"
ADMIN_PASSWORD = "burki4509"

DATA_FILE = "admin_stats.json"

# ================== VERİ YÜKLE ==================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "total_visits": 0,
            "total_clicks": 0,
            "last_visit": None
        }
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ================== SESSION INIT ==================
if "auth" not in st.session_state:
    st.session_state.auth = False

# ================== LOGIN EKRANI ==================
if not st.session_state.auth:
    st.set_page_config(page_title="Admin Giriş", layout="centered")

    st.markdown("## 🔐 Yapımcı Girişi")
    st.markdown("Bu sayfa sadece yetkili kullanıcı içindir.")

    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Şifre", type="password")

    if st.button("Giriş Yap"):
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("❌ Email veya şifre hatalı")

    st.stop()

# ================== PANEL ==================
st.set_page_config(page_title="Burak GPT • Admin Panel", layout="wide")

data = load_data()

# ziyaret sayısını admin girişiyle artırmak istemiyorsan burayı yorum satırı yapabilirsin
data["total_visits"] += 1
data["last_visit"] = datetime.now().strftime("%d.%m.%Y %H:%M")
save_data(data)

# ================== UI ==================
st.title("📊 Burak GPT • Yapımcı Paneli")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="👥 Toplam Ziyaret",
        value=data["total_visits"]
    )

with col2:
    st.metric(
        label="🖱️ Toplam Tıklanma",
        value=data["total_clicks"]
    )

with col3:
    st.metric(
        label="🕒 Son Giriş",
        value=data["last_visit"]
    )

st.divider()

# ================== AKSİYONLAR ==================
st.subheader("⚙️ Yönetim Araçları")

c1, c2 = st.columns(2)

with c1:
    if st.button("➕ Tıklanma Ekle"):
        data["total_clicks"] += 1
        save_data(data)
        st.success("Tıklanma artırıldı")
        st.rerun()

with c2:
    if st.button("🧹 İstatistikleri Sıfırla"):
        data = {
            "total_visits": 0,
            "total_clicks": 0,
            "last_visit": None
        }
        save_data(data)
        st.warning("Tüm istatistikler sıfırlandı")
        st.rerun()

st.divider()

# ================== HAM VERİ ==================
with st.expander("📦 Ham Veri (JSON)"):
    st.json(data)

st.caption("🛠️ Bu panel sadece yapımcıya özeldir.")
