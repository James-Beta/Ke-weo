import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="GDP Analysis",
    layout="wide"
)

df = pd.read_csv("data/Processed/gdp.csv")
df['Year'] = df['Year'].astype(str)
st.line_chart(df,
               x = 'Year', 
               y = 'GDP (Trillions KES)', 
               color="#00eeff",
               x_label= "YEAR",
               y_label= "GDP in trillions of Ksh",
               height='stretch')