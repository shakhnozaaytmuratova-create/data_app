import streamlit as st

st.set_page_config(layout="wide")

# =========================
# LANGUAGE STATE
# =========================

if "lang" not in st.session_state:
    st.session_state["lang"] = "English"

# =========================
# SIDEBAR (CLEAN + PREMIUM)
# =========================

st.sidebar.title("🚀 Data Wrangler")

st.sidebar.markdown("---")

# Language switch (pill style simplified)
st.sidebar.subheader("🌍 Language")

lang = st.sidebar.radio(
    "",
    ["English", "Русский", "O'zbek"],
    index=["English","Русский","O'zbek"].index(st.session_state["lang"])
)

st.session_state["lang"] = lang

st.sidebar.markdown("---")

st.sidebar.info("Use the menu above to navigate pages")

# =========================
# TEXTS
# =========================

texts = {
    "English": {
        "welcome": "Welcome to AI-Assisted Data Wrangler & Visualizer",
        "subtitle": "Clean, transform, and visualize your data like a pro 🚀",
        "start": "Start by uploading your dataset 👈",
    },
    "Русский": {
        "welcome": "Добро пожаловать в AI Data Wrangler & Visualizer",
        "subtitle": "Очистка и визуализация данных 🚀",
        "start": "Начните с загрузки данных 👈",
    },
    "O'zbek": {
        "welcome": "AI Data Wrangler & Visualizer ga xush kelibsiz",
        "subtitle": "Ma'lumotlarni tozalang va vizualizatsiya qiling 🚀",
        "start": "Boshlash uchun fayl yuklang 👈",
    }
}

t = texts[st.session_state["lang"]]

# =========================
# STYLE (CLEAN HERO)
# =========================

st.markdown("""
<style>
.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: #4A90E2;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    margin-bottom: 30px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background: #f5f7fa;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================

st.markdown(f'<div class="title">{t["welcome"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{t["subtitle"]}</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================
# FEATURES (IMPROVED)
# =========================

st.subheader("✨ What this app can do")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
    📂 <b>Upload</b><br>
    CSV, Excel, JSON, Google Sheets
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    🧹 <b>Clean</b><br>
    Missing values, duplicates, scaling, outliers
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
    📊 <b>Visualize</b><br>
    Interactive charts with filters & insights
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.success(t["start"])