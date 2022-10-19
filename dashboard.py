import streamlit as st
from PIL import Image
from route import plot_ports
from plaatje import plaatje
from get_ports_list import get_ports_list
import pandas as pd

st.title("Container passport")

xls = pd.ExcelFile("data/Dataset-data-interoperability_rev-HA.xlsx")
containers = pd.read_excel(xls, xls.sheet_names[0])["Containernummer"]

with st.sidebar:
    container = st.selectbox("Container", containers)

col1, col2 = st.columns(2)

with col1:
    shipping_ports, customs_ports = get_ports_list(container)
    fig, ax = plot_ports(shipping_ports, customs_ports, unloc=True)
    st.pyplot(fig)

with col2:
    ship_image_file = plaatje(container)
    image = Image.open(ship_image_file)
    st.image(image, caption="container ship", use_column_width="auto")
