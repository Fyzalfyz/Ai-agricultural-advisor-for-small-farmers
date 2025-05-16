import requests
import statistics
from datetime import datetime, timedelta

class WeatherAnalyzer:
    def __init__(self, api_key="c59af85b5caea78569d616126ca7928e"):
        self.api_key = api_key
        self.current_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.geocode_url = "https://api.openweathermap.org/geo/1.0/reverse"

    def get_weather_data(self, city_name):
        try:
            current = self._fetch_current_weather(city_name)
            forecast = self._fetch_hourly_forecast(city_name)
            
            return {
                "temperature_data": self._analyze_temperature(current, forecast),
                "humidity_data": self._analyze_humidity(current, forecast),
                "weather_conditions": self._analyze_conditions(current, forecast),
                "water_management": self._analyze_water_management(current),
                "historical_patterns": self._analyze_patterns(forecast)
            }
        except Exception as e:
            return {"error": str(e)}

    def _fetch_current_weather(self, city_name):
        params = {"q": city_name, "appid": self.api_key, "units": "metric"}
        response = requests.get(self.current_url, params=params)
        return response.json()

    def _fetch_hourly_forecast(self, city_name):
        params = {"q": city_name, "appid": self.api_key, "units": "metric"}
        response = requests.get(self.forecast_url, params=params)
        return response.json()

    def _analyze_temperature(self, current, forecast):
        temps = [item['main']['temp'] for item in forecast['list'][:8]]
        return {
            "current": current['main']['temp'],
            "forecast": [{"time": item['dt_txt'], "temp": item['main']['temp']} 
                        for item in forecast['list'][:8]],
            "max": max(temps),
            "min": min(temps),
            "avg": round(statistics.mean(temps), 1),
            "trend": "rising" if temps[-1] > temps[0] else "falling"
        }

    def _analyze_humidity(self, current, forecast):
        humidity_data = [item['main']['humidity'] for item in forecast['list'][:8]]
        return {
            "current": current['main']['humidity'],
            "forecast": [{"time": item['dt_txt'], "humidity": item['main']['humidity']} 
                        for item in forecast['list'][:8]],
            "high_humidity_hours": sum(1 for h in humidity_data if h > 70) * 3,
            "trend": "rising" if humidity_data[-1] > humidity_data[0] else "falling"
        }

    def _analyze_conditions(self, current, forecast):
        return {
            "current": current['weather'][0]['description'],
            "forecast": [{"time": item['dt_txt'], "condition": item['weather'][0]['description']} 
                        for item in forecast['list'][:8]],
            "precipitation_probability": self._calculate_precipitation_probability(forecast)
        }

    def _analyze_water_management(self, current):
        return {
            "temperature": current['main']['temp'],
            "humidity": current['main']['humidity'],
            "wind_speed": current['wind']['speed'],
            "conditions": current['weather'][0]['description']
        }

    def _analyze_patterns(self, forecast):
        rain_data = [forecast.get('rain', {}).get('3h', 0) for forecast in forecast['list'][:8]]
        temps = [item['main']['temp'] for item in forecast['list'][:8]]
        return {
            "total_rainfall": sum(rain_data),
            "temp_range": {"min": min(temps), "max": max(temps)},
            "temp_trend": "rising" if temps[-1] > temps[0] else "falling"
        }

    def _calculate_precipitation_probability(self, forecast):
        rain_count = sum(1 for item in forecast['list'][:8] if 'rain' in item)
        return round((rain_count / 8) * 100, 1)

def get_weather_based_recommendations(forecast_data):
    """
    Analyze weather forecast and return crop recommendations
    """
    try:
        # Aggregate weather conditions
        conditions = {
            'temps': [],
            'conditions': [],
            'dates': []
        }
        
        for day in forecast_data['forecast']:
            conditions['temps'].append(day['temp'])
            conditions['conditions'].append(day['condition'])
            conditions['dates'].append(day['date'])
        
        avg_temp = sum(conditions['temps']) / len(conditions['temps'])
        weather_summary = f"""
Next 7 days weather analysis:
Temperature Range: {min(conditions['temps'])}°C to {max(conditions['temps'])}°C
Average Temperature: {round(avg_temp, 1)}°C
Weather Conditions: {', '.join(set(conditions['conditions']))}
Forecast Period: {conditions['dates'][0]} to {conditions['dates'][-1]}
"""
        return weather_summary
        
    except Exception as e:
        print(f"Error in get_weather_based_recommendations: {str(e)}")
        return None

def get_7_day_forecast(city):
    """
    Return a 7-day forecast with crop recommendations
    """
    try:
        api_key = "c59af85b5caea78569d616126ca7928e"
        base_url = "https://api.openweathermap.org/data/2.5/forecast"
        
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",  # Use metric units for Celsius
            "cnt": 40  # Get maximum data points (5 days * 8 points per day)
        }
        
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code != 200:
            return {"error": data.get("message", "Failed to fetch weather data")}
            
        # Group forecast by day
        daily_forecasts = {}
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            if date not in daily_forecasts:
                daily_forecasts[date] = {
                    'temps': [],
                    'conditions': []
                }
            daily_forecasts[date]['temps'].append(item['main']['temp'])
            daily_forecasts[date]['conditions'].append(item['weather'][0]['description'])
        
        # Create 7-day forecast
        forecast = []
        current_date = datetime.now()
        
        for i in range(7):
            next_date = current_date + timedelta(days=i)
            date_str = next_date.strftime('%Y-%m-%d')
            
            # If we have data for this date, use it
            if date_str in daily_forecasts:
                avg_temp = sum(daily_forecasts[date_str]['temps']) / len(daily_forecasts[date_str]['temps'])
                # Get most common condition for the day
                condition = max(set(daily_forecasts[date_str]['conditions']), key=daily_forecasts[date_str]['conditions'].count)
            else:
                # For days beyond the API's forecast, use the last available data
                last_date = list(daily_forecasts.keys())[-1]
                avg_temp = sum(daily_forecasts[last_date]['temps']) / len(daily_forecasts[last_date]['temps'])
                condition = max(set(daily_forecasts[last_date]['conditions']), key=daily_forecasts[last_date]['conditions'].count)
            
            forecast.append({
                "date": date_str,
                "day": next_date.strftime("%A"),
                "temp": round(avg_temp),
                "condition": condition
            })
        
        forecast_data = {"forecast": forecast}
        
        # Get weather summary for recommendations
        weather_summary = get_weather_based_recommendations(forecast_data)
        if weather_summary:
            forecast_data["weather_summary"] = weather_summary
            
        return forecast_data
        
    except Exception as e:
        print(f"Error in get_7_day_forecast: {str(e)}")  # Add debug logging
        return {"error": str(e)}
