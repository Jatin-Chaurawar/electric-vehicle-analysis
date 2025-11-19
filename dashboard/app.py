# dashboard/app.py
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

ROOT = Path(__file__).parents[1]
df = pd.read_csv(ROOT/"data"/"processed"/"ev_population_features.csv")

st.title("EV Population Dashboard")

# State filter
state = st.selectbox(
    "Filter by state",
    options=["All"] + sorted(df["State"].dropna().unique().tolist())
)

if state != "All":
    dff = df[df["State"] == state]
else:
    dff = df

# -----------------------------
# 1️⃣ Top 10 Makes Bar Chart
# -----------------------------
top_makes = (
    dff["Make"]
    .value_counts()
    .head(10)
    .reset_index()
)

# Rename columns PROPERLY
top_makes.columns = ["Make", "Count"]

fig = px.bar(
    top_makes,
    x="Make",
    y="Count",
    title="Top EV Makes by Count"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 2️⃣ Trend Over Model Year
# -----------------------------
ts = (
    dff.groupby("Model Year")
    .size()
    .reset_index(name="Count")
    .sort_values("Model Year")
)

fig2 = px.line(
    ts,
    x="Model Year",
    y="Count",
    markers=True,
    title="EV Registrations Over Years"
)

st.plotly_chart(fig2, use_container_width=True)
