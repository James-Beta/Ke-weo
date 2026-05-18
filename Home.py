import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Kenya Economic Outlook",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

st.header("Kenya Economic outlook",divider=True)

from pyfonts import load_google_font, set_default_font
font = load_google_font("Funnel Sans")
font_bold = load_google_font("Funnel Sans", weight=800)
set_default_font(font)

st.markdown(
    "This project is geared towards providing an overview of how the Kenyan economy has been performing over the past few years and possibly how it will look in the coming years. "
    )
st.markdown(
    "All the data used is captured from free official sources such as the National Treasury, The Central Bank of Kenya(CBK) as well as any other official publications from international organisations such as the International Monetrary Fund (IMF)"
    )
st.write("You can find the raw data used in the [Public Github repository](https://github.com/James-Beta/Ke-weo) hosting this project, or you can download up-to-date versions directly from their sites" )

col1,col2,col3 = st.columns(3, gap="small")
with col1:
    st.link_button("The Central Bank of Kenya", "https://www.centralbank.go.ke/")
with col2:
    st.link_button("The National Treasury", "https://www.treasury.go.ke/")
with col3:
    st.link_button("The Internertional Monetary Fund", "https://data.imf.org/en")