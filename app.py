import streamlit as st
import pandas as pd
import plotly.express as px

st.image("https://www.nasa.gov/sites/default/files/thumbnails/image/nasa-logo-web-rgb.png", width=100)
st.title("🚀 NASA Exoplanet Discovery Dashboard")
st.markdown("Discover candidate exoplanets using AI + NASA Kepler data")

# Load predictions (must exist in artifacts folder)
df = pd.read_csv("artifacts/top_unlabeled_predictions.csv")

st.subheader("🌌 3D Candidate Planet Visualization")
fig = px.scatter_3d(
    df.head(50),
    x="koi_period",
    y="koi_duration",
    z="koi_depth",
    size="koi_period",
    color="score",
    hover_data=["kepoi_name", "score"]
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🔝 Top 10 Candidates")
st.dataframe(df.head(10))
