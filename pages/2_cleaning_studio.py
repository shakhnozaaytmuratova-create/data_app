import streamlit as st
import pandas as pd

st.title("🧹 Cleaning & Preparation Studio")

# =========================
# CHECK DATA EXISTS
# =========================

if "df" not in st.session_state:
    st.warning("Upload data first in Page A.")
    st.stop()

df = st.session_state["df"]

# Initialize log if missing
if "log" not in st.session_state:
    st.session_state["log"] = []

# =========================
# DATA PREVIEW
# =========================

st.subheader("🔍 Current Dataset Preview")
st.dataframe(df.head())

st.markdown("---")

# =========================
# MISSING VALUES SECTION
# =========================

with st.expander("⚠️ Missing Values Handling", expanded=True):

    missing_summary = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": df.isnull().sum().values,
        "Missing %": (df.isnull().mean() * 100).round(2).values
    })

    st.dataframe(missing_summary)

    selected_col = st.selectbox("Select column", df.columns)

    method = st.selectbox(
        "Choose method",
        ["Mean", "Median", "Mode", "Constant", "Drop Rows"]
    )

    constant_value = None

    if method == "Constant":
        constant_value = st.text_input("Enter replacement value")

    if st.button("Apply Missing Value Treatment"):

        before_missing = df[selected_col].isnull().sum()

        try:
            if method == "Mean":
                df[selected_col] = df[selected_col].fillna(df[selected_col].mean())

            elif method == "Median":
                df[selected_col] = df[selected_col].fillna(df[selected_col].median())

            elif method == "Mode":
                df[selected_col] = df[selected_col].fillna(df[selected_col].mode()[0])

            elif method == "Constant":
                df[selected_col] = df[selected_col].fillna(constant_value)

            elif method == "Drop Rows":
                df = df.dropna(subset=[selected_col])

            after_missing = df[selected_col].isnull().sum()

            st.session_state["df"] = df

            st.session_state["log"].append({
                "operation": "Missing Value Treatment",
                "column": selected_col,
                "method": method
            })

            st.success(f"Done. Missing values before: {before_missing}, after: {after_missing}")

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

# =========================
# DUPLICATES SECTION
# =========================

with st.expander("📎 Duplicate Handling"):

    duplicate_count = df.duplicated().sum()
    st.info(f"Duplicate rows found: {duplicate_count}")

    keep_option = st.selectbox(
        "Keep duplicate option",
        ["first", "last"]
    )

    if st.button("Remove Duplicates"):

        before_rows = df.shape[0]

        df = df.drop_duplicates(keep=keep_option)

        after_rows = df.shape[0]

        st.session_state["df"] = df

        st.session_state["log"].append({
            "operation": "Remove Duplicates",
            "keep": keep_option
        })

        st.success(f"Removed {before_rows - after_rows} duplicate rows.")

st.markdown("---")

# =========================
# TRANSFORMATION LOG
# =========================

st.subheader("📜 Transformation Log")

if st.session_state["log"]:
    log_df = pd.DataFrame(st.session_state["log"])
    st.dataframe(log_df)
else:
    st.info("No transformations applied yet.")