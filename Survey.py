# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import csv
import os
import pandas as pd
import streamlit as st

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Bridgerton Favorites Survey 📝")
st.write("Please fill out the form below stating your favorite Bridgerton Ship and your rating for it on a scale of 1-10")

# File path definition (ensures correct directory location relative to root)
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "..", "data.csv")

# 1. Initialize data.csv with column headers if it does not exist yet
if not os.path.exists(csv_path):
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Ships", "Value"])

# DATA INPUT FORM
with st.form("survey_form", clear_on_submit=True):
    category_input = st.text_input("Enter a category:")
    value_input = st.text_input("Enter a corresponding value:")

    submitted = st.form_submit_button("Submit Data")

    # Runs ONLY when the submit button is clicked
    if submitted:
        if not category_input.strip() or not value_input.strip():
            st.error("Please enter both a Category and a Value before submitting!")
        else:
            # 2. Append new row to data.csv in append ('a') mode
            with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([category_input.strip(), value_input.strip()])

            st.success("Your data has been submitted!")
            st.write(
                f"You entered: **Category:** {category_input}, **Value:** {value_input}"
            )

# DATA DISPLAY
st.divider()
st.header("Current Data in CSV")

# Read and display data.csv contents
if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
    current_data_df = pd.read_csv(csv_path)
    st.dataframe(current_data_df, use_container_width=True)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
