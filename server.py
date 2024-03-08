import requests
import os
import json

api_key = os.getenv('API_KEY')


def get_coordinates(city_name):
    """
    Gets Coordinates of City from OpenWeatherMap Geocoding API
    :param city_name: The city name from which to get latitude and longitude values.
    :return lat lon: Return the latitude and longitude of the city.
    """
    #https://openweathermap.org/api/geocoding-api
    api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={api_key}"
    try:
    #https://www.geeksforgeeks.org/response-reason-python-requests/?ref=lbp
        response = requests.get(api_url)
        response.raise_for_status()
        response_data = response.json()
        
        lat = response_data[0]["lat"]
        lon = response_data[0]["lon"]

        return lat, lon
    #https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
    #https://openweathermap.org/faq#error401
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            print(f"HTTP ERROR 401: API Key expired, missing or Invalid. {err}") 
        if err.response.status_code == 404:
            print(f"HTTP ERROR 404: Could not find specified city. {err}") 
        if err.response.status_code == 429:
            print(f"HTTP ERROR 429: Surpassing the limit of your subscription of 60 API calls per minute. {err}")
        if err.response.status_code == 500 or err.response.status_code == 502 or err.response.status_code == 503 or err.response.status_code == 504:
            print(f"HTTP ERROR {err.response.status_code}: Contact OpenWeatherMap for assistance. {err}") 
        
    except KeyError:
        print("DATA ERROR: Could not use response data for Geolocation, check response and index")
        

def get_weather(lat, lon):
    """
    Gets weather data from OpenWeatherMap Current Weather data API using latitude and longitude provided by Geocoding API
    :param lat: The latitude of the location.
    :param lon: The longitude of the location.
    :return temperature: Return the temperature for the specified city.
    """
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

def get_city_name_from_config(config_file='config.json'):
    """
    Reads the city name from a configuration file.
    :param config_file: The path to the configuration.json file
    :return: The city name read from the file.
    """
    with open(config_file, 'r') as file:
        config_dict = json.load(file)
        return config_dict["city_name"]
    

if __name__ == "__main__":
    
    city_name = get_city_name_from_config()
    
    lat, lon = get_coordinates(city_name)
    
    temperature = get_weather(lat, lon)
    print(f"Temperature in {city_name} is {temperature}°C")