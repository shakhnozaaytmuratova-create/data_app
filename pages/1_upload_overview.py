import streamlit as st
import pandas as pd

@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

@st.cache_data
def load_excel(file):
    return pd.read_excel(file)

st.set_page_config(layout="wide")

st.title("📂 Upload & Data Overview")

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

# =========================
# STYLE
# =========================

st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 15px;
    background: #f8f9fb;
    margin-bottom: 20px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
}
.step-title {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION
# =========================

df = st.session_state.get("df", None)

# =========================
# STEP 1 — DATA SOURCE
# =========================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="step-title">① Select Data Source</div>', unsafe_allow_html=True)

data_source = st.radio(
    "Choose how to load your data",
    ["Upload File", "Google Sheets"],
    horizontal=True
)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# STEP 2 — UPLOAD
# =========================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="step-title">② Load Dataset</div>', unsafe_allow_html=True)

if data_source == "Upload File":

    uploaded_file = st.file_uploader(
        "Upload CSV / Excel / JSON",
        type=["csv", "xlsx", "json"]
    )

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)

            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)

            elif uploaded_file.name.endswith(".json"):
                df = pd.read_json(uploaded_file)

            st.session_state["df"] = df.copy()
            st.session_state["original_df"] = df.copy()

            if "log" not in st.session_state:
                st.session_state["log"] = []

            st.success("✅ File uploaded successfully")

        except Exception as e:
            st.error(f"Error: {e}")

else:
    url = st.text_input("Paste Google Sheets URL")

    if url:
        try:
            sheet_id = url.split("/d/")[1].split("/")[0]
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

            df = pd.read_csv(csv_url)

            st.session_state["df"] = df.copy()
            st.session_state["original_df"] = df.copy()

            st.success("✅ Google Sheet loaded")

        except:
            st.error("Invalid link")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# STEP 3 — DATA SUMMARY
# =========================

if "df" in st.session_state:

    df = st.session_state["df"]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">③ Dataset Summary</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # STEP 4 — TABS (CLEAN VIEW)
    # =========================

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">④ Explore Data</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Preview",
        "Data Types",
        "Missing Values",
        "Duplicates"
    ])

    with tab1:
        st.dataframe(df.head(50))

    with tab2:
        dtypes = df.dtypes.reset_index()
        dtypes.columns = ["Column", "Type"]
        st.dataframe(dtypes)

    with tab3:
        missing = pd.DataFrame({
            "Column": df.columns,
            "Missing Count": df.isnull().sum().values,
            "Missing %": (df.isnull().mean() * 100).round(2).values
        })
        st.dataframe(missing)

    with tab4:
        duplicates = df.duplicated().sum()
        st.metric("Duplicate Rows", duplicates)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# RESET
# =========================

if st.button("🔄 Reset Session"):

    st.session_state.clear()

    # reset uploader key (IMPORTANT)
    st.session_state["uploader_key"] = st.session_state.get("uploader_key", 0) + 1

    st.rerun()