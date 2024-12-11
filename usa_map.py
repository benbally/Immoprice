# Import libraries

import pandas as pd
import folium
import streamlit as st
import streamlit.components.v1 as components
import requests


# Downlod hosuing market dataset from drive and loading it 
# The dataset includes location, price, number of bedrooms and bathrooms and house size of properties that are currently for sale in the USA
# For the USA Map, data on property price was used to display the average property price in a given city and the the amount of available properties per city was counted from the dataset

url = f"https://www.dropbox.com/scl/fi/wou0utc59c1gs4j3tmfvo/USA-data-reduced2.csv?rlkey=k467ardnwmrsjuz7g4to3iv76&st=ky08kmzi&dl=1"
response = requests.get(url)
with open("USA-data.zip.csv", "wb") as f:
    f.write(response.content)
df = pd.read_csv("USA-data.zip.csv")

# List the top 20 largest U.S. cities by population together with their coordinates, population and the state they are located in
# These 20 cities will be available in the application

top20_cities = [
    {"name": "New York City", "lat": 40.7128, "lon": -74.0060, "population": 8335897, "state": "New York"},
    {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "population": 3822238, "state": "California"},
    {"name": "Chicago", "lat": 41.8781, "lon": -87.6298, "population": 2665039, "state": "Illinois"},
    {"name": "Houston", "lat": 29.7604, "lon": -95.3698, "population": 2302878, "state": "Texas"},
    {"name": "Phoenix", "lat": 33.4484, "lon": -112.0740, "population": 1644409, "state": "Arizona"},
    {"name": "Philadelphia", "lat": 39.9526, "lon": -75.1652, "population": 1567258, "state": "Pennsylvania"},
    {"name": "San Antonio", "lat": 29.4241, "lon": -98.4936, "population": 1472909, "state": "Texas"},
    {"name": "San Diego", "lat": 32.7157, "lon": -117.1611, "population": 1381162, "state": "California"},
    {"name": "Dallas", "lat": 32.7767, "lon": -96.7970, "population": 1299544, "state": "Texas"},
    {"name": "Austin", "lat": 30.2672, "lon": -97.7431, "population": 974447, "state": "Texas"},
    {"name": "Jacksonville", "lat": 30.3322, "lon": -81.6557, "population": 971319, "state": "Florida"},
    {"name": "San Jose", "lat": 37.3382, "lon": -121.8863, "population": 971233, "state": "California"},
    {"name": "Fort Worth", "lat": 32.7555, "lon": -97.3308, "population": 956709, "state": "Texas"},
    {"name": "Columbus", "lat": 39.9612, "lon": -82.9988, "population": 907971, "state": "Ohio"},
    {"name": "Charlotte", "lat": 35.2271, "lon": -80.8431, "population": 897720, "state": "North Carolina"},
    {"name": "Indianapolis", "lat": 39.7684, "lon": -86.1581, "population": 880621, "state": "Indiana"},
    {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194, "population": 808437, "state": "California"},
    {"name": "Seattle", "lat": 47.6062, "lon": -122.3321, "population": 749256, "state": "Washington"},
    {"name": "Denver", "lat": 39.7392, "lon": -104.9903, "population": 713252, "state": "Colorado"},
    {"name": "Washington", "lat": 38.9072, "lon": -77.0369, "population": 678972, "state": "District of Columbia"}
]


# Add a heading and subheading for the page  

st.markdown("<h1 style='text-align: center; margin-bottom: -30px;'>Your starting point in the USA</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>Find the perfect city for your needs</h3>", unsafe_allow_html=True)


# Inset a radio button to select the currency used to display the average property price in a given city

currency = st.radio("Select Currency:", ("🇺🇸 USD", "🇨🇭 CHF"))


# Create a map and set the initial center position to the geographic center of the USA

usa_map = folium.Map(location=[39.8282, -98.5795], zoom_start=4)


# Iterate over the top 20 cities, retrieving relevant information and adding a pin marker (which diplays this information in a popup) for each city

for city in top20_cities:
    city_name = city["name"]
    city_state = city["state"]
    city_population = city["population"]
    city_lat = city["lat"]
    city_lon = city["lon"]
    

    # Retrieve weather data from the Weatherstack API

    weather_params = {
        "access_key": "f76cce61bafada2ba3e18faaee48e4d7" ,
        "query": f"{city_name}, USA",
        "units": "m"
    }
    
    weather_response = requests.get("http://api.weatherstack.com/current", params=weather_params)
    weather_data = weather_response.json()
    
    weather_info = weather_data.get("current", {})
    temperature = weather_info.get("temperature", "N/A")
    weather_description = weather_info.get("weather_descriptions", ["N/A"])[0]

    
    # Calculate the average property price for the top 20 cities using the housing market dataset

    city_data = df[df["city"].str.contains(city_name, na=False)]

    if not city_data.empty:
        average_price =int(city_data["price"].mean())

    else:
        average_price = None
    

    # Use the Amdoren API to convert the average property price from USD to CHF if the user has selected CHF as the display currency

    if currency == "🇨🇭 CHF":   
        response = requests.get(f"https://www.amdoren.com/api/currency.php?api_key=C7AecWnwHkC5rCV9eg65sf2V5FjzpF&from=USD&to=CHF&amount={average_price}")
        average_price_display = response.json().get("amount")
        average_price_display = f"CHF {average_price_display:,.0f}" if average_price else "N/A"

    else:
        average_price_display = f"${average_price:,.0f}" if average_price else "N/A"
    

    # Count properties available for sale from the housing market dataset

    property_count = df[df["city"].str.contains(city_name, na=False)].shape[0]
    

    # Define information for each city (City Name, State, Population, Current Weather, Average Property Price and Number of Properties available for Sale)

    popup_content = f"""
    <div style="font-size: 14px;">
        <strong>City:</strong> {city_name}<br>
        <strong>State:</strong> {city_state}<br>
        <strong>Population:</strong> {city_population:,}<br>
        <strong>Current Weather:</strong> {temperature} °C, {weather_description}<br>
        <strong>Average Property Price:</strong> {average_price_display}<br>
        <strong>Properties available for Sale:</strong> {property_count:,}
    </div>
"""


 # Add a pin marker for each of the top 20 cities at the corresponding coordinates, displaying the corresponding city information

    folium.Marker(
        location=[city_lat, city_lon],
        popup=folium.Popup(popup_content, max_width= 280),
        tooltip=city_name,
        icon=folium.Icon(icon="city", prefix="fa", color="red")
    ).add_to(usa_map)


# Display the map

components.html(usa_map._repr_html_(), height=600)
