import streamlit as st
from PIL import Image
import os

# Seitenleiste für Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["USA Map", "Property Price Estimator"])

# Dynamisches Laden der Seiten
if page == "USA Map":
    file_path = os.path.join("usa_map.py")
    with open(file_path, encoding="utf-8") as file:
        exec(file.read(), globals())

else:
    file_path = os.path.join("streamlitapp.py")
    with open(file_path, encoding="utf-8") as file:
        exec(file.read(), globals())
