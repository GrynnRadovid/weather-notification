import requests
import sys
import os

api_key = os.getenv('API_KEY')


def get_coordinates(city_name):
    """Gets Geolocation of City from OpenWeatherMap Geolocation API"""
    #https://openweathermap.org/api/geocoding-api
    api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={api_key}"

    #https://www.geeksforgeeks.org/response-reason-python-requests/?ref=lbp
    response = requests.get(api_url)
    response_data = response.json()

    if response_data:
        lat = response_data[0]["lat"]
        print(lat)
        lon = response_data[0]["lon"]
        print(lon)
        return lat, lon
    else:
        print("ERROR")


def get_weather(lat, lon):
    """Gets weather data from OpenWeatherMap Current Weather data API"""
    #https://openweathermap.org/current
    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    #https://www.geeksforgeeks.org/response-reason-python-requests/?ref=lbp
    response = requests.get(api_url)
    response_data = response.json()

    if response_data:
        temperature = response_data["main"]["temp"]
        return temperature
    else:
        print("ERROR")

if __name__ == "__main__":
    
    city_name = sys.argv[1]
    
    lat, lon = get_coordinates(city_name)
    
    temperature = get_weather(lat, lon)
    print(f"Temperature in {city_name} is {temperature}°C")