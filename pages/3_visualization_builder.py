import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(layout="wide")

# =========================
# LANGUAGE FIX
# =========================
lang = st.session_state.get("lang", "English")

# =========================
# DARK MODE
# =========================
dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    plt.style.use("dark_background")
else:
    sns.set_style("whitegrid")

st.title("📊 Visualization Builder (Matplotlib)")

# =========================
# CHECK DATA
# =========================
if "df" not in st.session_state:
    st.warning("Upload dataset first")
    st.stop()

df = st.session_state["df"].copy()

# fix numeric
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="ignore")

numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(include="object").columns.tolist()

# =========================
# AUTO DASHBOARD
# =========================

st.subheader("📈 Automatic Insights")

col1, col2 = st.columns(2)

# BAR (AGGREGATED)
with col1:
    if categorical_cols and numeric_cols:

        grouped = df.groupby(categorical_cols[0])[numeric_cols[0]].mean()

        fig, ax = plt.subplots()
        grouped.plot(kind="bar", ax=ax)

        ax.set_title("Average Value by Category")
        ax.set_xlabel(categorical_cols[0])
        ax.set_ylabel(numeric_cols[0])

        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("Download Bar Chart", buf.getvalue(), "bar.png")

# LINE
with col2:
    if numeric_cols:

        fig, ax = plt.subplots()
        ax.plot(df[numeric_cols[0]])

        ax.set_title("Trend Over Index")
        ax.set_xlabel("Index")
        ax.set_ylabel(numeric_cols[0])

        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("Download Line Chart", buf.getvalue(), "line.png")

# SCATTER
if len(numeric_cols) > 1:

    fig, ax = plt.subplots()
    ax.scatter(df[numeric_cols[0]], df[numeric_cols[1]])

    ax.set_title("Relationship Between Variables")
    ax.set_xlabel(numeric_cols[0])
    ax.set_ylabel(numeric_cols[1])

    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("Download Scatter Plot", buf.getvalue(), "scatter.png")

st.markdown("---")

# =========================
# AI SUGGESTION
# =========================

st.subheader("🤖 AI Suggestions")

if st.button("Suggest Visualization"):

    if categorical_cols and numeric_cols:
        st.success("Use Bar Chart for category comparisons")

    if len(numeric_cols) > 1:
        st.success("Use Scatter Plot for relationships")

    if "date" in " ".join(df.columns).lower():
        st.success("Use Line Chart for time trends")

st.markdown("---")

# =========================
# CUSTOM BUILDER
# =========================

st.subheader("⚙️ Custom Chart Builder")

chart_type = st.selectbox(
    "Chart Type",
    ["Bar", "Line", "Scatter", "Histogram", "Box", "Heatmap", "3D Scatter"]
)

x_col = st.selectbox("X-axis", df.columns)
y_col = st.selectbox("Y-axis", numeric_cols)

# =========================
# BUILD CHART
# =========================

try:

    fig = plt.figure()

    # BAR
    if chart_type == "Bar":
        grouped = df.groupby(x_col)[y_col].mean()

        ax = fig.add_subplot(111)
        grouped.plot(kind="bar", ax=ax)

        ax.set_title("Bar Chart")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)

    # LINE
    elif chart_type == "Line":
        ax = fig.add_subplot(111)
        ax.plot(df[x_col], df[y_col])

        ax.set_title("Line Chart")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)

    # SCATTER
    elif chart_type == "Scatter":
        ax = fig.add_subplot(111)
        ax.scatter(df[x_col], df[y_col])

        ax.set_title("Scatter Plot")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)

    # HISTOGRAM
    elif chart_type == "Histogram":
        ax = fig.add_subplot(111)
        ax.hist(df[x_col], bins=20)

        ax.set_title("Distribution")
        ax.set_xlabel(x_col)

    # BOX
    elif chart_type == "Box":
        ax = fig.add_subplot(111)
        ax.boxplot(df[y_col])

        ax.set_title("Box Plot")
        ax.set_ylabel(y_col)

    # HEATMAP
    elif chart_type == "Heatmap":
        corr = df.corr(numeric_only=True)

        ax = fig.add_subplot(111)
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

        ax.set_title("Correlation Heatmap")

    # 3D SCATTER
    elif chart_type == "3D Scatter":
        z_col = st.selectbox("Z-axis", numeric_cols)

        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(df[x_col], df[y_col], df[z_col])

        ax.set_title("3D Scatter Plot")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_zlabel(z_col)

    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png")

    st.download_button("📥 Download Chart", buf.getvalue(), "chart.png")

except Exception as e:
    st.error(f"Chart error: {e}")