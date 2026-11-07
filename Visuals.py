# This creates the page for displaying data visualizations.

import streamlit as st
import pandas as pd
import altair as alt
import json
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# CUTE GIF BACKGROUND & FROSTED GLASS EFFECT From Youtube please give me extra credit---
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcGZ5bG1yNjRxdHB1MzVvYTR0YmFsYjY5N3ppM2F4ZmJkcDR3amJyNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Bd5eqkRxUY7OP94PWt/giphy.gif");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* Frosted glass background box so your text and charts stay readable over the GIF */
.block-container {
    background-color: rgba(255, 240, 245, 0.88);
    padding: 2rem;
    border-radius: 15px;
    margin-top: 2rem;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
import streamlit as st
import json
import os
import pandas as pd
import altair as alt

st.title("Bridgerton Seasons Epic lovers Rating (^o^)")
st.markdown("---")

current_dir = os.path.dirname(__file__)
json_path = os.path.join(current_dir, "..", "data.json")

with open(json_path) as infile:
    raw_data = json.load(infile)

labels = [item["label"] for item in raw_data["data_points"]]
values = [item["value"] for item in raw_data["data_points"]]

df = pd.DataFrame({
    "Category": labels,
    "Value": values
})

st.write("### 📊 Bridgerton Ratings")
st.bar_chart(data=df, x="Category", y="Value")

st.markdown("---")

st.write("### 🎛 Individual Ratings")

if "selected_cat" not in st.session_state:
    st.session_state.selected_cat = "All"

selected_category = st.selectbox(
    "Highlight a specific category:", 
    options=["All"] + list(df["Category"])
)

if selected_category != "All":
    filtered_df = df[df["Category"] == selected_category]
else:
    filtered_df = df

dynamic_chart = alt.Chart(filtered_df).mark_bar(color="#ff69b4", cornerRadius=6).encode(
    x=alt.X("Category:N", sort=None, axis=alt.Axis(labelAngle=0)),
    y="Value:Q"
).properties(
    title="Bridgerton Drama Ratings by Couple", 
    height=300
)

st.altair_chart(dynamic_chart, use_container_width=True)
# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
st.markdown("---")
st.title("📈 Part 2: Survey CSV Visualizations")

csv_path = os.path.join(current_dir, "..", "data.csv")

if os.path.exists(csv_path):
    df_csv = pd.read_csv(csv_path)

    if df_csv.empty:
        st.warning(
            "The `data.csv` file is currently empty. Please submit entries on the Survey page!"
        )
    else:
        # STATIC CSV VISUALIZATION 
        st.write("### 📈 Static CSV Chart: Data Trends (Line Chart)")
        st.line_chart(data=df_csv, x="Category", y="Value")

        st.markdown("---")

        #DYNAMIC CSV VISUALIZATION WITH SESSION STATE- pn: pie chart from link in canvas
        st.write("### 🎛 Dynamic CSV Chart: Category Distribution (Plotly Pie)")

        if "selected_csv_category" not in st.session_state:
            st.session_state.selected_csv_category = "All Categories"

        categories = ["All Categories"] + list(
            df_csv["Category"].dropna().unique()
        )
        selected_cat = st.radio(
            "Filter chart display by Category:",
            options=categories,
            key="selected_csv_category",
        )

        if st.session_state.selected_csv_category != "All Categories":
            filtered_csv_df = df_csv[
                df_csv["Category"] == st.session_state.selected_csv_category
            ]
        else:
            filtered_csv_df = df_csv

        category_counts = (
            filtered_csv_df["Category"].value_counts().reset_index()
        )
        category_counts.columns = ["Category", "Count"]

        #Plotly Express Pie Chart  from youtube vid xD
        fig_pie = px.pie(
            category_counts,
            values="Count",
            names="Category",
            title="Distribution of Submitted Survey Categories",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.3,  
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")

        st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.error(
        "`data.csv` file not found! Make sure `data.csv` exists in your project directory."
    )
