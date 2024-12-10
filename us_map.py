
#-----TO DO-----

#Currency API (Das dropdown menu für select currency hat im Moment noch keine Funktion)´
#Weather API gibt immer N/A
#Falls möglich die Karte speichern, sodass die nicht jedesmal neu lädt, wenn man die currency ändert


#Import libraries
import pandas as pd
import folium
import streamlit as st
import requests


#Load data set
data_path = "/Users/benjaminbally/desktop/USA-data.zip.csv"
df = pd.read_csv(data_path)


# Top 20 US cities
largest_cities = [
    {"name": "New York City", "lat": 40.7128, "lon": -74.0060, "population": 8419600, "state": "New York"},
    {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "population": 3980400, "state": "California"},
    {"name": "Chicago", "lat": 41.8781, "lon": -87.6298, "population": 2716000, "state": "Illinois"},
    {"name": "Houston", "lat": 29.7604, "lon": -95.3698, "population": 2328000, "state": "Texas"},
    {"name": "Phoenix", "lat": 33.4484, "lon": -112.0740, "population": 1690000, "state": "Arizona"},
    {"name": "Philadelphia", "lat": 39.9526, "lon": -75.1652, "population": 1584200, "state": "Pennsylvania"},
    {"name": "San Antonio", "lat": 29.4241, "lon": -98.4936, "population": 1547253, "state": "Texas"},
    {"name": "San Diego", "lat": 32.7157, "lon": -117.1611, "population": 1423851, "state": "California"},
    {"name": "Dallas", "lat": 32.7767, "lon": -96.7970, "population": 1341075, "state": "Texas"},
    {"name": "San Jose", "lat": 37.3382, "lon": -121.8863, "population": 1021795, "state": "California"},
    {"name": "Austin", "lat": 30.2672, "lon": -97.7431, "population": 964254, "state": "Texas"},
    {"name": "Jacksonville", "lat": 30.3322, "lon": -81.6557, "population": 911507, "state": "Florida"},
    {"name": "Fort Worth", "lat": 32.7555, "lon": -97.3308, "population": 936000, "state": "Texas"},
    {"name": "Columbus", "lat": 39.9612, "lon": -82.9988, "population": 905748, "state": "Ohio"},
    {"name": "Charlotte", "lat": 35.2271, "lon": -80.8431, "population": 872498, "state": "North Carolina"},
    {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194, "population": 870887, "state": "California"},
    {"name": "Indianapolis", "lat": 39.7684, "lon": -86.1581, "population": 876384, "state": "Indiana"},
    {"name": "Seattle", "lat": 47.6062, "lon": -122.3321, "population": 744955, "state": "Washington"},
    {"name": "Denver", "lat": 39.7392, "lon": -104.9903, "population": 715522, "state": "Colorado"},
    {"name": "Washington", "lat": 38.9072, "lon": -77.0369, "population": 705749, "state": "District of Columbia"}
]



# Weatherstack API Setup
weather_api_key = "260fafda710c5c1d558cf10fa0f1336e"  # API-Schlüssel
weather_base_url = "http://api.weatherstack.com/current"


#Add title
st.markdown("<h1 style='text-align: center; margin-bottom: -15px;'>Your starting point in the USA</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-top: -15px; margin-bottom: 30px;'>Find the perfect city for your needs</h3>", unsafe_allow_html=True)



#Calculate average price per city
def calculate_avg_price(city):
    city_data = df[df["city"].str.contains(city, case=False, na=False)]
    if not city_data.empty:
        return city_data["price"].mean()
    return None


# Radio-Button Selection
währung = st.radio("Select Currency:", ("🇺🇸 USD", "🇨🇭 CHF"))
    

#Import map
us_cities_map = folium.Map(location=[39.0902, -97.6129], zoom_start=4)

for city in largest_cities:
    city_name = city["name"]
    city_lat = city["lat"]
    city_lon = city["lon"]
    city_population = city["population"]
    city_state = city["state"]
    

    # Retrieve weather data
    weather_params = {
        "access_key": weather_api_key,
        "query": f"{city_name}, USA",
        "units": "m"
    }
    weather_response = requests.get(weather_base_url, params=weather_params)
    weather_data = weather_response.json()
    

    # Making sure weather data is available
    if "current" in weather_data:
        weather_info = weather_data["current"]
        temperature = weather_info.get("temperature", "N/A")
        weather_desc = weather_info.get("weather_descriptions", ["N/A"])[0]
    else:
        temperature = "N/A"
        weather_desc = "N/A"

    
    #Calculate average property price
    avg_price = calculate_avg_price(city_name)
    

    # API query: Conversion of the predicted price from dollars to CHF if the user has specified CHF as the selection 

    if währung == "🇨🇭 CHF":   
        response = requests.get(f"https://www.amdoren.com/api/currency.php?api_key=C7AecWnwHkC5rCV9eg65sf2V5FjzpF&from=USD&to=CHF&amount={avg_price}")
        avg_price_display = response.json().get("amount")
        avg_price_display = f"CHF {avg_price_display:,.2f}" if avg_price else "N/A"

    else:
        avg_price_display = f"${avg_price:,.2f}" if avg_price else "N/A"
    

    # Get the number of available properties
    num_properties = df[df["city"].str.contains(city_name, case=False, na=False)].shape[0]
    

    # Pop-up-Details
    popup_content = f"""
    <div style="font-size: 14px;">
        <strong>City:</strong> {city_name}<br>
        <strong>State:</strong> {city_state}<br>
        <strong>Population:</strong> {city_population:,}<br>
        <strong>Weather:</strong> {temperature} °C, {weather_desc}<br>
        <strong>Average Property Price:</strong> {avg_price_display}<br>
        <strong>Properties Available:</strong> {num_properties:,}
    </div>
"""


    # Add pin marker
    folium.Marker(
        location=[city_lat, city_lon],
        popup=folium.Popup(popup_content, max_width=300),
        tooltip=city_name,
        icon=folium.Icon(icon="city", prefix="fa", color="red")
    ).add_to(us_cities_map)



# Display map
st.components.v1.html(us_cities_map._repr_html_(), height=600)
