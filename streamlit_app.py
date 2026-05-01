import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Stock peer analysis dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

from pyfonts import load_google_font, set_default_font
font = load_google_font("Funnel Sans")
font_bold = load_google_font("Funnel Sans", weight=800)
set_default_font(font)
pd.options.display.float_format = '{:.4f}'.format
df = pd.read_csv("data/ke_weo_imf.csv", index_col="INDICATOR")
df['SCALE.ID'] = pd.to_numeric(df['SCALE.ID'], errors='coerce')
multiplier = 10 ** df['SCALE.ID']
df[['2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025','2026']] = df[['2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025','2026']].mul(multiplier, axis=0)
indicators = df[['2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025','2026']]
indicators = indicators[~indicators.index.str.contains('dollar', na=False)]
gdp_values = indicators.loc['Gross domestic product (GDP), Constant prices, Domestic currency']
gdp_values = gdp_values/1000000000000
# use the plot function
fig, ax = plt.subplots(dpi=200)
ax.set_title("Gross domestic product (GDP), Constant prices, Trillions (KES)")
for i, value in enumerate(gdp_values):
    ax.text(
        x=i,
        y=value,
        s=f"Ksh{value:.2f}T",
        bbox=dict(facecolor="white", alpha=0.9),
        zorder=100,
    )
plt.plot(gdp_values, color="black")
ax.spines[["top", "left", "right"]].set_visible(False)
ax.tick_params(axis="x", pad=5, size=10)
ax.tick_params(axis="y", size=0)
ax.grid(axis="y", zorder=-2, alpha=0.3)

st.pyplot(fig)