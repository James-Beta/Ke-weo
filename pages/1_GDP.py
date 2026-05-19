import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="GDP Analysis",
    layout="wide"
)

df = pd.read_csv("data/Processed/gdp.csv")
df['Year'] = df['Year'].astype(str)
col1, col2 = st.columns([4, 1])
col1.line_chart(df,
               x = 'Year', 
               y = 'GDP (Trillions KES)', 
               color="#00eeff",
               x_label= "YEAR",
               y_label= "GDP in trillions of Ksh",
               height='content')
col2.dataframe(df, hide_index=True)