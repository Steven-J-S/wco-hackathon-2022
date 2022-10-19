import streamlit as st
from PIL import Image
from coordinates import plot_ports
import pandas as pd

st.title("Container route")

xls = pd.ExcelFile("data/Dataset-data-interoperability_rev-HA.xlsx")
containers = pd.read_excel(xls, xls.sheet_names[0])["Containernummer"]
container = st.selectbox("Container", containers)
st.write(container)

fig, ax = plot_ports(["NLRTM", "CNXMG", "CNNBG"])
st.pyplot(fig)

image = Image.open("ship.jpg")
st.image(image, caption="container ship MEARSK DAANIS", use_column_width="auto")
