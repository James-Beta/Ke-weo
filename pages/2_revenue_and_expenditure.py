import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Government Revenue & Spending",
    layout="wide")


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
