import yfinance as yf
import time
import pandas as pd
from kafka import KafkaProducer
from json import dumps
import requests

def get_weather_data(lat, lon, api_key):
    # Base URL for OpenWeatherMap One Call API
    url = 'https://api.openweathermap.org/data/3.0/onecall'

    # Parameters for the API call
    params = {
        'lat': lat,
        'lon': lon,
        'exclude': 'hourly,daily',  # Exclude hourly and daily data
        'appid': api_key,
        'units': 'metric'  # Optional: use 'imperial' for Fahrenheit, 'metric' for Celsius
    }

    # Make the API call
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the JSON response
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def kafka_producer():
    producer = KafkaProducer(bootstrap_servers=['34.227.190.251:9092'], # change ip and port number here
    value_serializer=lambda x: dumps(x).encode('utf-8'))

    t_end = time.time() + 60 * 1 # Amount of time data is sent for in seconds

    while time.time() < t_end:
        # Replace with your actual API key
        api_key = 'cba60f2181e5014b7668f6fede64a3b7'

        # Coordinates for the location

        latitude = 45.618997524
        longitude = 9.286998852

        data = get_weather_data(latitude, longitude, api_key)
        producer.send('WeatherData', value=data) # Add topic name here
    print("done producing")

kafka_producer()
