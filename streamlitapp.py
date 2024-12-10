import streamlit as st
import pandas as pd
import joblib
import requests

# Top 20 Städte
top20_cities = [
    "New York City", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "Austin",
    "Jacksonville", "San Jose", "Fort Worth", "Columbus", "Charlotte",
    "Indianapolis", "San Francisco", "Seattle", "Denver", "Washington"
]

# Laden des Modells, Scalers und LabelEncoders
@st.cache_resource
def load_model_and_scalers():
    model = joblib.load("finalizedmodel.pkl")
    scaler = joblib.load("scaler.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
    return model, scaler, label_encoder

model, scaler, label_encoder = load_model_and_scalers()

# User input
bedrooms = st.number_input("Number of Bedrooms:", min_value=1, step=1, value=1)
bathrooms = st.number_input("Number of Bathrooms:", min_value=1, step=1, value=1)
house_size = st.number_input("House Size (in sqft):", min_value=1, step=1, value=1000)
city = st.selectbox("Select City:", top20_cities)

# Coding the city with LabelEncoder, so model works
city_encoded = label_encoder.transform([city])[0]

# Erstelle DataFrame mit den Eingabedaten
user_input = pd.DataFrame(
    [[bedrooms, bathrooms, city_encoded, house_size]],
    columns=["bed", "bath", "city", "house_size"]
)

# Skalieren der Eingabedaten
user_input_scaled = scaler.transform(user_input)

# Vorhersage durchführen
predicted_price = model.predict(user_input_scaled)
predicted_price = float(predicted_price[0])

# Radio-Button Selection
währung = st.radio("Select Currency:", ("🇺🇸 USD", "🇨🇭 CHF"))


# API query: Conversion of the predicted price from dollars to CHF if the user has specified CHF as the selection 

if währung == "🇨🇭 CHF":   
    response = requests.get(f"https://www.amdoren.com/api/currency.php?api_key=C7AecWnwHkC5rCV9eg65sf2V5FjzpF&from=USD&to=CHF&amount={predicted_price}")
    avg_price_display = response.json().get("amount")
    avg_price_display = float(avg_price_display)
    avg_price_display = f"CHF {avg_price_display:,.2f}" 

else:
    avg_price_display = f"${predicted_price:,.2f}"

    
#Text Box
st.markdown(f"""
    <div style="border: 1px solid #4CAF50; padding: 8px; border-radius: 8px; background-color: #f9f9f9; max-width: 400px; margin: 0 auto;">
        <h3 style="text-align: center; color: #4CAF50;">Estimated Price:</h3>
        <h2 style="text-align: center; color: #000;">{avg_price_display}</h2>
    </div>
""", unsafe_allow_html=True)
