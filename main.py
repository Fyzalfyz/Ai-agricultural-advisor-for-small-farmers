import requests

# Constants (from config.py)
API_KEY = "c59af85b5caea78569d616126ca7928e"
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_WEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Weather functions (from weather.py)
def fetch_current_weather(city_name):
    """Fetch current weather data for a given city."""
    try:
        params = {"q": city_name, "appid": API_KEY, "units": "metric"}
        response = requests.get(CURRENT_WEATHER_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Error fetching current weather: {e}")

def fetch_hourly_forecast(city_name):
    """Fetch hourly forecast data for a given city."""
    try:
        params = {"q": city_name, "appid": API_KEY, "units": "metric"}
        response = requests.get(FORECAST_WEATHER_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Error fetching hourly forecast: {e}")

# Utility functions (from utils.py)
def display_current_weather(data):
    """Format and display current weather data."""
    city = data["name"]
    temperature = data["main"]["temp"]
    weather = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    print(f"\nCity: {city}")
    print(f"Temperature: {temperature}°C")
    print(f"Weather: {weather.capitalize()}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")

def display_hourly_forecast(data):
    """Format and display hourly weather forecast for the next 24 hours."""
    print("\nHourly Weather Forecast (Next 24 Hours):")
    for forecast in data["list"][:8]:  # 8 intervals for the next 24 hours (3-hour intervals)
        time = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        weather_desc = forecast["weather"][0]["description"]
        print(f"{time}: {temp}°C, {weather_desc.capitalize()}")

# Main function
def main():
    print("Real-Time Weather Application")
    city_name = input("Enter the city name: ")

    # Fetch and display current weather
    current_weather = fetch_current_weather(city_name)
    display_current_weather(current_weather)

    # Fetch and display hourly forecast
    hourly_forecast = fetch_hourly_forecast(city_name)
    display_hourly_forecast(hourly_forecast)

if __name__ == "__main__":
    main()
