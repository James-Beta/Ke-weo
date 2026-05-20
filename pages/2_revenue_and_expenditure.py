import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Government Revenue & Spending",
    layout="wide")

revenue_df = pd.read_csv("data/Processed/rev.csv", parse_dates=['Period'])
# Create a radio button so the user can choose their timeframe scale
view_mode = st.radio(
    "Select Timeframe View", 
    ["Single Month", "Single Year", "Custom Range"], 
    horizontal=True
)

if view_mode == "Single Month":
    # Extract unique months formatted nicely (e.g., "Jan 1999")
    available_months = revenue_df['Period'].dt.strftime('%b %Y').unique()
    
    # Default to the most recent month (the last item in the array)
    selected_month = st.selectbox("Select Month", available_months, index=len(available_months)-1)
    chart_title = f"Money Flow for {selected_month}"
    
    # Filter where the formatted date matches the selection
    mask = revenue_df['Period'].dt.strftime('%b %Y') == selected_month

elif view_mode == "Single Year":
    # Extract unique years and sort them
    available_years = sorted(revenue_df['Period'].dt.year.unique())
    
    # Default to the most recent year
    selected_year = st.selectbox("Select Year", available_years, index=len(available_years)-1)
    chart_title = f"Money Flow for {selected_year}"
    # Filter where the year matches the selection
    mask = revenue_df['Period'].dt.year == selected_year

else: # Custom Range
    min_date = revenue_df['Period'].min().date()
    max_date = revenue_df['Period'].max().date()
    
    # Use Streamlit's native calendar picker instead of a slider for range
    selected_dates = st.date_input(
        "Select Date Range", 
        value=(min_date, max_date), 
        min_value=min_date, 
        max_value=max_date
    )
    chart_title = f"Money Flow starting {selected_dates[0].strftime('%b %Y')}"
    
    # Error handling: date_input returns a tuple of 1 if the user hasn't clicked the end date yet
    if len(selected_dates) == 2:
        mask = (revenue_df['Period'].dt.date >= selected_dates[0]) & (revenue_df['Period'].dt.date <= selected_dates[1])
    else:
        # If they only clicked a start date, just show that single day/month
        mask = revenue_df['Period'].dt.date == selected_dates[0]

# Apply the mask to create the specific data for the Sankey
filtered_df = revenue_df.loc[mask]

st.markdown("### Money Flow: Revenue to Expenditure")


# ==========================================
# 2. PREP THE SANKEY DATA
# ==========================================
# Define exactly which columns represent our inflows and outflows
revenue_sources = [
    'Import Duty', 'Excise Duty', 'Income Tax', 'VAT', 
    'Other Tax Income', 'Non-Tax Revenue', 'Programme Grants', 'Project Grants'
]

expenditure_targets = [
    'Domestic Interest', 'Foreign Interest', 'Wages & Salaries', 
    'Pensions', 'Other Recurrent', 'County Transfer', 'Development Expenditure'
]

# Calculate the totals for the selected period
# (Using .sum() aggregates the data over the selected months)
flow_data = filtered_df[revenue_sources + expenditure_targets].sum()

# Define the Nodes (The labels that will appear on the screen)
# Index 0-7 are revenues, Index 8 is the central pool, Index 9-15 are expenditures
nodes = revenue_sources + ['Consolidated Fund (Total)'] + expenditure_targets
center_node_index = len(revenue_sources) # This will be 8

# Define the Links (The flows from Source to Target)
sources = []
targets = []
values = []

# Flow 1: All individual Revenue Sources -> Flow into the Consolidated Fund (Node 8)
for i in range(len(revenue_sources)):
    sources.append(i)               # The individual tax/grant
    targets.append(center_node_index) # The center pool
    values.append(flow_data[revenue_sources[i]]) # The total Ksh value

# Flow 2: Consolidated Fund (Node 8) -> Flows out to Expenditure Targets
for i in range(len(expenditure_targets)):
    sources.append(center_node_index) # The center pool
    targets.append(center_node_index + 1 + i) # The specific expenditure category
    values.append(flow_data[expenditure_targets[i]]) # The total Ksh value


# ==========================================
# 3. DRAW THE SANKEY DIAGRAM
# ==========================================
fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 20,       # Spacing between nodes
      thickness = 30, # Thickness of the node block
      line = dict(color = "black", width = 0.5),
      label = nodes,
      # Adding some custom colors (Greens for money in, Grey for pool, Reds/Oranges for money out)
      color = ["#2a9d8f"] * len(revenue_sources) + ["#264653"] + ["#e76f51"] * len(expenditure_targets)
    ),
    link = dict(
      source = sources,
      target = targets,
      value = values,
      # Optional: Make the links slightly transparent so they look like flowing water
      color = "rgba(169, 169, 169, 0.4)" 
    )
)])

fig.update_layout(
    title_text=chart_title,
    font_size=12,
    height=600 # Give it plenty of vertical room to breathe
)

st.plotly_chart(fig, use_container_width=True)
# Render the dataframe with a visual mask over the Period column
if st.button("Show Data"):
    st.markdown("### Raw Data (Millions, Ksh)")
    
    revenue_df = pd.read_csv("data/Processed/rev.csv")
    
    st.dataframe(
        revenue_df,
        column_config={
            "Period": st.column_config.DatetimeColumn(
                "Reporting Month",
                format="MMMM YYYY",
            )
        },
        hide_index=True
    )
