
# Job Alert Bot - Auto-Refreshing Web App with GitHub Scheduler

import streamlit as st
import pandas as pd
import os

DATA_FILE = "daily_jobs.csv"

st.title("Job Alert Bot - Daily Refreshed")
st.write("Auto-updated daily with job listings from BDJobs, BPSC, and BD Bank")

# --- Display Cached Results (Fetched Daily) ---
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)

    st.success(f"Showing {len(df)} jobs (auto-updated daily)")

    # --- Filters ---
    sources = st.multiselect("Filter by source:", options=df['Source'].unique(), default=list(df['Source'].unique()))
    companies = st.multiselect("Filter by company:", options=df['Company'].unique(), default=list(df['Company'].unique()))
    categories = st.multiselect("Filter by category:", options=df['Category'].unique(), default=list(df['Category'].unique()))
    deadlines = st.multiselect("Filter by deadline:", options=df['Deadline'].unique(), default=list(df['Deadline'].unique()))

    filtered_df = df[
        (df['Source'].isin(sources)) &
        (df['Company'].isin(companies)) &
        (df['Category'].isin(categories)) &
        (df['Deadline'].isin(deadlines))
    ]

    st.write(f"Filtered jobs: {len(filtered_df)}")
    st.dataframe(filtered_df)

    # CSV Export
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "jobs.csv", "text/csv")
else:
    st.warning("Job data file not found. Waiting for daily update...")
