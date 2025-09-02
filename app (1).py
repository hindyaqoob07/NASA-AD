import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Branding ---
st.image("https://www.nasa.gov/sites/default/files/thumbnails/image/nasa-logo-web-rgb.png", width=120)
st.title("🚀 NASA Exoplanet Discovery Dashboard")
st.markdown("Discover candidate exoplanets using AI + NASA Kepler data")

# --- Load predictions ---
csv_path = "artifacts/top_unlabeled_predictions.csv"
if not os.path.exists(csv_path):
    st.error("❌ Predictions file not found. Please ensure artifacts/top_unlabeled_predictions.csv exists.")
    st.stop()

df = pd.read_csv(csv_path)

# --- Sidebar Controls ---
st.sidebar.header("🔧 Controls")
min_score = st.sidebar.slider("Minimum Confidence", 0.0, 1.0, 0.8, 0.01)
max_candidates = st.sidebar.number_input("Max candidates to show", 10, 200, 50, 10)
view = st.sidebar.radio("Choose view", ["3D Visualization", "Candidate Table"])

df_filtered = df[df["score"] >= min_score]

# --- Main Display ---
if view == "3D Visualization":
    st.subheader("🌌 3D Candidate Planet Visualization")
    if df_filtered.empty:
        st.warning("No candidates above selected confidence threshold.")
    else:
        fig = px.scatter_3d(
            df_filtered.head(max_candidates),
            x="koi_period",
            y="koi_duration",
            z="koi_depth",
            size="koi_period",
            color="score",
            hover_data=["kepoi_name", "score"]
        )
        fig.update_layout(scene=dict(
            xaxis_title='Orbital Period',
            yaxis_title='Transit Duration',
            zaxis_title='Transit Depth'
        ))
        st.plotly_chart(fig, use_container_width=True)

else:
    st.subheader("🔝 Top Candidates (Filtered)")
    if df_filtered.empty:
        st.warning("No candidates above selected confidence threshold.")
    else:
        st.dataframe(df_filtered.head(max_candidates))

# --- Extra Insights ---
st.markdown("---")
st.subheader("📈 Precision-Recall Curve")
if os.path.exists("artifacts/pr_curve.png"):
    st.image("artifacts/pr_curve.png", caption="Validation PR Curve")
else:
    st.info("PR curve image not found.")

st.subheader("🔍 SHAP Feature Importance")
if os.path.exists("artifacts/shap_summary.png"):
    st.image("artifacts/shap_summary.png", caption="Feature importance from SHAP")
else:
    st.info("SHAP summary not found.")

st.markdown("✅ End of dashboard")
