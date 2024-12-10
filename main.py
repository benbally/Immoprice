import streamlit as st
from PIL import Image


# Seitenleiste für Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["USA Map", "Property Price Estimator"])

# Lade die entsprechenden Seiten
if page == "USA Map":
    # Importiere die Logik aus us_map.py
    import immoprice.pages.us_map
elif page == "Property Price Estimator":
    # Importiere die Logik aus streamlitapp.py
    import immoprice.pages.streamlitapp
