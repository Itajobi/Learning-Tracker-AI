import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Set file path
DATA_PATH = "learning_data.csv"

# Load data
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=["Course", "Category", "Status", "Start Date", "End Date", "Notes"])

# Save data
def save_data(data):
    data.to_csv(DATA_PATH, index=False)

# Load existing data
df = load_data()
df['Category'] = df['Category'].astype(str).str.strip()
df['Status'] = df['Status'].astype(str).str.strip()

# --- APP HEADER ---
st.title("📘 Learning Tracker AI")
st.subheader("Track your learning progress")

# --- FILTER SECTION ---
with st.expander("🔍 Filter Learning Data"):
    selected_category = st.multiselect("Filter by Category", options=sorted(df['Category'].unique()), default=sorted(df['Category'].unique()))
    selected_status = st.multiselect("Filter by Status", options=sorted(df['Status'].unique()), default=sorted(df['Status'].unique()))
    filtered_df = df[(df["Category"].isin(selected_category)) & (df["Status"].isin(selected_status))]

# --- VIEW DATA ---
with st.expander("📊 View Current Learning Data"):
    st.dataframe(filtered_df)

# --- INPUT FORM ---
st.subheader("➕ Add New Learning Entry")
with st.form("entry_form"):
    course = st.text_input("Course")
    category = st.selectbox("Category", ["Programming", "Data Visualization", "Version Control", "Data Science", "Other"])
    status = st.selectbox("Status", ["Completed", "In Progress", "Not Started"])
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date (optional)", value=None)
    notes = st.text_area("Notes")

    submitted = st.form_submit_button("Add Entry")
    if submitted:
        new_row = {
            "Course": course,
            "Category": category.strip(),
            "Status": status.strip(),
            "Start Date": start_date,
            "End Date": end_date if end_date else "",
            "Notes": notes
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("✅ New learning entry added!")
        st.rerun()  # refresh the app

# --- DELETE ENTRY ---
st.subheader("🗑️ Remove an Entry")

if len(df) > 0:
    df_display = df.reset_index().copy()
    df_display["Label"] = df_display["Course"] + " | " + df_display["Category"] + " | " + df_display["Status"]
    option = st.selectbox("Select entry to remove:", df_display["Label"])

    if st.button("Delete Selected Entry"):
        index_to_remove = df_display[df_display["Label"] == option]["index"].values[0]
        df = df.drop(index=index_to_remove).reset_index(drop=True)
        save_data(df)
        st.success("❌ Entry deleted successfully.")
        st.rerun()
else:
    st.info("No entries to delete.")
