import requests
from datetime import datetime, timedelta
import statistics

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

def analyze_temperature_patterns(forecast_data):
    """Analyze temperature patterns from forecast data."""
    temps = [item['main']['temp'] for item in forecast_data['list'][:8]]
    return {
        'max_temp': max(temps),
        'min_temp': min(temps),
        'avg_temp': statistics.mean(temps),
        'trend': 'rising' if temps[-1] > temps[0] else 'falling'
    }

def analyze_humidity_patterns(forecast_data):
    """Analyze humidity patterns and high humidity periods."""
    humidity_data = [item['main']['humidity'] for item in forecast_data['list'][:8]]
    high_humidity_count = sum(1 for h in humidity_data if h > 70)
    return {
        'avg_humidity': statistics.mean(humidity_data),
        'high_humidity_hours': high_humidity_count * 3,
        'trend': 'rising' if humidity_data[-1] > humidity_data[0] else 'falling'
    }

def calculate_precipitation_probability(forecast_data):
    """Calculate precipitation probability from forecast data."""
    rain_count = sum(1 for item in forecast_data['list'][:8] if 'rain' in item)
    return (rain_count / 8) * 100

def display_weather_analysis(current_weather, hourly_forecast):
    """Display comprehensive weather analysis."""
    temp_patterns = analyze_temperature_patterns(hourly_forecast)
    humidity_patterns = analyze_humidity_patterns(hourly_forecast)
    precip_prob = calculate_precipitation_probability(hourly_forecast)

    print("\n1. Temperature Data")
    print("-" * 50)
    print(f"- Current Temperature: {current_weather['main']['temp']}°C")
    print("- 24-Hour Temperature Forecast:")
    for forecast in hourly_forecast['list'][:8]:
        print(f"  {forecast['dt_txt']}: {forecast['main']['temp']}°C")
    print(f"- Temperature Patterns:")
    print(f"  Max: {temp_patterns['max_temp']}°C")
    print(f"  Min: {temp_patterns['min_temp']}°C")
    print(f"  Average: {temp_patterns['avg_temp']:.1f}°C")
    print(f"  Trend: {temp_patterns['trend']}")

    print("\n2. Humidity Information")
    print("-" * 50)
    print(f"- Current Humidity: {current_weather['main']['humidity']}%")
    print("- Humidity Forecast:")
    for forecast in hourly_forecast['list'][:8]:
        print(f"  {forecast['dt_txt']}: {forecast['main']['humidity']}%")
    print(f"- High Humidity Duration: {humidity_patterns['high_humidity_hours']} hours")
    print(f"- Humidity Trend: {humidity_patterns['trend']}")

    print("\n3. Weather Conditions")
    print("-" * 50)
    print(f"- Current Weather: {current_weather['weather'][0]['description'].capitalize()}")
    print("- 24-Hour Weather Forecast:")
    for forecast in hourly_forecast['list'][:8]:
        print(f"  {forecast['dt_txt']}: {forecast['weather'][0]['description'].capitalize()}")
    print(f"- Precipitation Probability: {precip_prob:.1f}%")

    print("\n4. Water Management Enhancement")
    print("-" * 50)
    print(f"- Current Temperature: {current_weather['main']['temp']}°C")
    print(f"- Current Humidity: {current_weather['main']['humidity']}%")
    print(f"- Wind Speed: {current_weather['wind']['speed']} m/s")
    print(f"- Current Conditions: {current_weather['weather'][0]['description'].capitalize()}")

    print("\n5. Historical Patterns")
    print("-" * 50)
    print("- Recent Rainfall Data:")
    rain_data = [forecast.get('rain', {}).get('3h', 0) for forecast in hourly_forecast['list'][:8]]
    print(f"  Total Expected Rainfall: {sum(rain_data):.1f}mm")
    print("- Temperature Trend:")
    print(f"  Direction: {temp_patterns['trend']}")
    print(f"  Range: {temp_patterns['min_temp']}°C to {temp_patterns['max_temp']}°C")
    print("- Humidity Pattern:")
    print(f"  Average: {humidity_patterns['avg_humidity']:.1f}%")
    print(f"  Trend: {humidity_patterns['trend']}")

# Main function
def main():
    print("Real-Time Weather Analysis Application")
    city_name = input("Enter the city name: ")

    try:
        current_weather = fetch_current_weather(city_name)
        hourly_forecast = fetch_hourly_forecast(city_name)
        display_weather_analysis(current_weather, hourly_forecast)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
