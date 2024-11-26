import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
stumpage_url = "https://raw.githubusercontent.com/azd169/timber_prices/main/ms_stumpage.csv"
stumpage = pd.read_csv(stumpage_url)

# Add a 'Time' column for easier filtering
stumpage["Time"] = stumpage["Year"].astype(str) + " " + stumpage["Quarter"]

# Set up the Streamlit app
st.set_page_config(page_title="Mississippi Timber Price Report", layout="wide")

# Header
st.title("Mississippi Timber Price Report")
st.write("""
The Mississippi Timber Price Report provides a snapshot of timber market activity, 
showing statewide stumpage prices for common forest products.
""")

# Sidebar filters
st.sidebar.header("Filters")
price_selector = st.sidebar.radio("Select Price Metric:", ["Minimum", "Average", "Maximum"], index=1)
type_selector = st.sidebar.multiselect("Select Type(s):", stumpage["Type"].unique())
quarter_selector = st.sidebar.multiselect("Select Quarter(s):", ["Q1", "Q2", "Q3", "Q4"])
year_range = st.sidebar.slider(
    "Select Year Range:",
    int(stumpage["Year"].min()),
    int(stumpage["Year"].max()),
    (int(stumpage["Year"].min()), int(stumpage["Year"].max())),
)

# Filter the data
filtered_data = stumpage[
    (stumpage["Type"].isin(type_selector) if type_selector else True) &
    (stumpage["Quarter"].isin(quarter_selector) if quarter_selector else True) &
    (stumpage["Year"] >= year_range[0]) &
    (stumpage["Year"] <= year_range[1])
]

# Plot data
if filtered_data.empty:
    st.warning("No data available for the selected filters.")
else:
    fig = px.line(
        filtered_data,
        x="Time",
        y=price_selector,
        color="Type",
        labels={"Time": "Time", price_selector: "Price ($/ton)", "Type": "Type"},
        title="Mississippi Timber Prices Over Time",
    )
    fig.update_traces(marker=dict(size=6), line=dict(width=2))
    fig.update_layout(
        legend=dict(
            orientation="h",  # Horizontal orientation
            x=0.5,            # Centre the legend horizontally
            xanchor="center", # Anchor legend horizontally at the centre
            y=-0.3,           # Move the legend slightly lower
            yanchor="top"     # Align the legend's top edge with the specified `y` position
        )
    )
    st.plotly_chart(fig, use_container_width=True)


# Download button for filtered data
st.download_button(
    label="Download Filtered Data as CSV",
    data=filtered_data.to_csv(index=False),
    file_name="filtered_timber_data.csv",
    mime="text/csv",
)

# Footer
st.markdown("""
For further assistance, contact [Sabhyata Lamichhane](mailto:Sabhyata.lamichhane@msstate.edu).
""")
